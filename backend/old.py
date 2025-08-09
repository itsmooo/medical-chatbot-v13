from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from pymongo import MongoClient
from datetime import datetime
import logging
from dotenv import load_dotenv
import time
import numpy as np
from collections import Counter

# Try to import OpenAI for symptom validation
try:
    import openai
    OPENAI_AVAILABLE = True
    print("✅ OpenAI imported successfully")
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not available - symptom validation will be skipped")

# Try to import TensorFlow for deep neural network
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
    print("✅ TensorFlow imported successfully")
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not available - deep neural network model will be skipped")

from deep_translator import GoogleTranslator


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client for symptom validation
openai_client = None
if OPENAI_AVAILABLE:
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if openai.api_key:
            openai_client = openai
            logger.info("✅ OpenAI client initialized successfully")
        else:
            logger.warning("⚠️ OPENAI_API_KEY not found in environment variables")
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
        openai_client = None

# Import Somali precautions
try:
    from precautions import disease_precautions
    logger.info("✅ Successfully imported Somali precautions")
except ImportError as e:
    logger.error(f"❌ Failed to import precautions: {e}")
    disease_precautions = {}

# Import disease rules for Somali symptom analysis
try:
    from disease_rules import DISEASE_RULES
    logger.info("✅ Successfully imported disease rules")
except ImportError as e:
    logger.error(f"❌ Failed to import disease rules: {e}")
    DISEASE_RULES = {}

# Initialize Deep Translator with better error handling
try:
    # Test basic translation
    test_translator = GoogleTranslator(source='en', target='en')
    # Check if the method is async
    import inspect
    if inspect.iscoroutinefunction(test_translator.translate):
        import asyncio
        test_result = asyncio.run(test_translator.translate('hello world'))
    else:
        test_result = test_translator.translate('hello world')
    logger.info(f'✅ Deep Translator test successful: EN->EN = "{test_result}"')
    
    # Test Somali translation
    somali_translator = GoogleTranslator(source='en', target='so')
    if inspect.iscoroutinefunction(somali_translator.translate):
        test_somali = asyncio.run(somali_translator.translate('hello world'))
    else:
        test_somali = somali_translator.translate('hello world')
    logger.info(f'✅ Deep Translator Somali test: EN->SO = "{test_somali}"')
    
    # Set up global translator for auto-detection
    translator = GoogleTranslator(source='auto', target='en')
    logger.info('✅ Deep Translator initialized successfully')
    
except Exception as e:
    logger.error(f'❌ Failed to initialize Deep Translator: {str(e)}')
    translator = None

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:8080'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# MongoDB setup
# Initialize MongoDB collections as None first
predictions_collection = None
feedback_collection = None
chat_messages_collection = None

try:
    # Try to connect to MongoDB with a timeout to avoid hanging
    mongo_uri = os.getenv('MONGODB_URI', 'mongodb+srv://mohamedadan:1234@cluster0.4bijvlo.mongodb.net/medicalDB')
    logger.info(f'Attempting to connect to MongoDB at {mongo_uri}')
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Force a connection to verify it works
    client.server_info()
    
    db = client.DiseasePrediction
    predictions_collection = db.predictions
    feedback_collection = db.feedback
    
    # Test inserting and retrieving a document to verify full functionality
    test_doc_id = predictions_collection.insert_one({'test': True, 'timestamp': datetime.utcnow()}).inserted_id
    test_doc = predictions_collection.find_one({'_id': test_doc_id})
    predictions_collection.delete_one({'_id': test_doc_id})
    
    # Create chat_messages collection if it doesn't exist
    if 'chat_messages' not in db.list_collection_names():
        db.create_collection('chat_messages')
        logger.info('Created chat_messages collection')
    chat_messages_collection = db.chat_messages
    
    if test_doc:
        logger.info('✅ MongoDB connection and CRUD operations verified successfully')
    else:
        logger.warning('⚠️ MongoDB connected but test document retrieval failed')
        
except Exception as e:
    logger.error(f'❌ MongoDB connection failed: {str(e)}')
    logger.error('Predictions and feedback will not be saved to the database!')
    # Keep the collections as None to indicate they're not available

# Load ALL AVAILABLE MODELS for Ensemble Prediction
models = {}
model_weights = {}

# Get the directory where this script is located for robust path handling
script_dir = os.path.dirname(os.path.abspath(__file__))

# Model 1: Scikit-learn model from models directory
try:
    models['sklearn'] = joblib.load(os.path.join(script_dir, 'models/disease_predictor.pkl'))
    model_weights['sklearn'] = 0.3
    logger.info("✅ Scikit-learn model loaded")
except Exception as e:
    logger.warning(f"⚠️ Failed to load scikit-learn model: {str(e)}")

# Model 2: Random Forest model from disease_models directory
try:
    models['random_forest'] = joblib.load(os.path.join(script_dir, 'disease_models/random_forest_model.pkl'))
    model_weights['random_forest'] = 0.3
    logger.info("✅ Random Forest model loaded")
except Exception as e:
    logger.warning(f"⚠️ Failed to load Random Forest model: {str(e)}")

# Model 3: SVM model from disease_models directory
try:
    models['svm'] = joblib.load(os.path.join(script_dir, 'disease_models/svm_model.pkl'))
    model_weights['svm'] = 0.2
    logger.info("✅ SVM model loaded")
except Exception as e:
    logger.warning(f"⚠️ Failed to load SVM model: {str(e)}")

# Model 4: Deep Neural Network model (if TensorFlow is available)
if TENSORFLOW_AVAILABLE:
    try:
        models['deep_nn'] = keras.models.load_model(os.path.join(script_dir, 'disease_models/deep_neural_network_model.h5'))
        model_weights['deep_nn'] = 0.2
        logger.info("✅ Deep Neural Network model loaded")
    except Exception as e:
        logger.warning(f"⚠️ Failed to load Deep Neural Network model: {str(e)}")

# Load preprocessing components
try:
    
    vectorizer = joblib.load(os.path.join(script_dir, 'models/tfidf_vectorizer.pkl'))
    
    # Try to load label encoder from disease_models first (for deep NN compatibility)
    try:
        label_encoder = joblib.load(os.path.join(script_dir, 'disease_models/label_encoder.pkl'))
        logger.info("✅ Loaded label encoder from disease_models directory")
    except FileNotFoundError:
        # Fallback to models directory
        label_encoder = joblib.load(os.path.join(script_dir, 'models/medical_label_encoder_20250609_203011.pkl'))
        logger.info("✅ Loaded label encoder from models directory")
    
    # Try to load feature scaler, but don't fail if it doesn't exist
    try:
        feature_scaler = joblib.load(os.path.join(script_dir, 'disease_models/feature_scaler.pkl'))
    except FileNotFoundError:
        feature_scaler = None
        logger.warning("⚠️ Feature scaler not found, deep NN model will be skipped")
    
    logger.info(f"✅ Preprocessing components loaded. Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
except Exception as e:
    logger.error(f"❌ Failed to load preprocessing components: {str(e)}")
    raise

# Verify we have at least one model
if not models:
    raise ValueError("No models could be loaded!")

logger.info(f"✅ Ensemble setup complete. Loaded {len(models)} models:")
for model_name, weight in model_weights.items():
    logger.info(f"   - {model_name}: weight {weight}")

# Disease-specific precautions (English)
DISEASE_PRECAUTIONS = {
    "Pneumonia": [
        "Take prescribed antibiotics or antiviral medications as directed by your doctor",
        "Get plenty of rest and avoid strenuous activities",
        "Drink plenty of fluids to stay hydrated and help loosen mucus",
        "Use a humidifier or breathe steam from a hot shower to ease breathing",
        "Avoid smoking and exposure to secondhand smoke",
        "Follow up with your healthcare provider as recommended"
    ],
    "Malaria": [
        "Take antimalarial medications exactly as prescribed by your doctor",
        "Use mosquito nets while sleeping, especially during night hours",
        "Apply insect repellent containing DEET to exposed skin",
        "Wear long-sleeved clothing and long pants during evening and night",
        "Seek immediate medical attention if symptoms worsen",
        "Complete the full course of treatment even if you feel better"
    ],
    "Diabetes": [
        "Monitor your blood sugar levels regularly as advised by your healthcare provider",
        "Follow a balanced diet and control carbohydrate intake",
        "Take prescribed medications (insulin or oral drugs) consistently",
        "Engage in regular physical activity as recommended by your doctor",
        "Check your feet daily for cuts, sores, or signs of infection",
        "Schedule regular check-ups for eye, kidney, and foot examinations"
    ],
    "Common Cold": [
        "Get adequate rest to help your body recover",
        "Stay well hydrated by drinking water, herbal teas, or warm broths",
        "Use a humidifier or inhale steam to relieve congestion",
        "Gargle with warm salt water to soothe a sore throat",
        "Wash hands frequently to prevent spreading the infection",
        "Avoid close contact with others to prevent transmission"
    ],
    "Migraine": [
        "Take prescribed migraine medications at the first sign of symptoms",
        "Rest in a quiet, dark, and cool room during an attack",
        "Apply a cold compress to your forehead or temples",
        "Identify and avoid known migraine triggers",
        "Maintain regular sleep and eating schedules",
        "Stay hydrated and manage stress levels"
    ]
}

# Generic precautions
GENERIC_PRECAUTIONS = [
    "Consult a healthcare professional immediately for proper diagnosis and treatment",
    "Follow your doctor's prescribed treatment plan carefully",
    "Monitor your symptoms and seek medical attention if they worsen",
    "Take prescribed medications exactly as directed",
    "Get adequate rest and maintain proper nutrition",
    "Stay hydrated and avoid self-medication"
]

def detect_language_fixed(text, lang_param='auto'):
    """
    MANUAL language selection instead of detection
    """
    try:
        logger.info(f"🔍 LANGUAGE SELECTION for: '{text[:50]}...'")
        logger.info(f"🌐 Manual language param: '{lang_param}'")
        
        # Manual language selection based on parameter
        if lang_param in ['som', 'somali', 'so']:
            logger.info("✅ MANUAL SELECTION: Somali language")
            return 'som'
        elif lang_param in ['en', 'english', 'eng']:
            logger.info("✅ MANUAL SELECTION: English language")
            return 'en'
        else:
            # Fallback: check for Somali keywords if auto mode
            somali_keywords = ['waxaan', 'qabaa', 'qandho', 'madax', 'xanuun', 'daal', 'haraad', 'kaadi']
            text_lower = text.lower()
            somali_found = sum(1 for keyword in somali_keywords if keyword in text_lower)
            
            if somali_found >= 1:
                logger.info(f"✅ FALLBACK: Detected as Somali (found {somali_found} keywords)")
                return 'som'
            else:
                logger.info(f"✅ FALLBACK: Detected as English (no Somali keywords)")
                return 'en'
            
    except Exception as e:
        logger.error(f"❌ Language selection failed: {str(e)}")
        return 'en'

def translate_text_fixed(text, source_lang, target_lang):
    """
    FIXED translation with proper language codes and debugging using deep_translator
    """
    try:
        logger.info(f"🔄 TRANSLATING: '{text[:50]}...' FROM {source_lang} TO {target_lang}")
        
        if translator is None:
            logger.warning("⚠️ Deep Translator not available")
            return text
        
        # Skip if same language
        if source_lang == target_lang:
            logger.info("⚠️ Same language, skipping translation")
            return text
        
        # FIXED: Correct language codes for deep_translator
        deep_source = 'so' if source_lang == 'som' else source_lang
        deep_target = 'so' if target_lang == 'som' else target_lang
        
        logger.info(f"🔄 Using Deep Translator codes: {deep_source} -> {deep_target}")
        
        # Create translator instance for this specific translation
        translator_instance = GoogleTranslator(source=deep_source, target=deep_target)
        
        # Translate - handle potential async issues
        try:
            # Try synchronous translation first
            translated_text = translator_instance.translate(text)
        except Exception as translate_error:
            logger.error(f"❌ Translation error: {str(translate_error)}")
            # Try with different approach - might be async
            try:
                # Create a new translator instance and try async if needed
                fallback_translator = GoogleTranslator(source=deep_source, target=deep_target)
                # Check if the method is async
                import inspect
                if inspect.iscoroutinefunction(fallback_translator.translate):
                    import asyncio
                    translated_text = asyncio.run(fallback_translator.translate(text))
                else:
                    translated_text = fallback_translator.translate(text)
            except Exception as fallback_error:
                logger.error(f"❌ Fallback translation also failed: {str(fallback_error)}")
                return text
        
        if translated_text and translated_text.strip():
            logger.info(f"✅ TRANSLATION SUCCESS: '{translated_text[:50]}...'")
            return translated_text.strip()
        else:
            logger.warning("⚠️ Empty translation result")
            return text
            
    except Exception as e:
        logger.error(f"❌ Translation failed: {str(e)}")
        return text

def translate_precautions_fixed(precautions_list, target_lang):
    """
    FIXED precautions translation with better error handling using deep_translator
    """
    if target_lang == 'en' or translator is None:
        logger.info(f"⚠️ No translation needed (target: {target_lang})")
        return precautions_list
    
    logger.info(f"🔄 TRANSLATING {len(precautions_list)} PRECAUTIONS TO {target_lang}")
    translated_precautions = []
    
    for i, precaution in enumerate(precautions_list):
        try:
            logger.info(f"🔄 Translating precaution {i+1}: '{precaution[:30]}...'")
            
            translated = translate_text_fixed(precaution, 'en', target_lang)
            translated_precautions.append(translated)
            
            logger.info(f"✅ Result {i+1}: '{translated[:30]}...'")
            
            # Rate limiting
            time.sleep(0.3)
            
        except Exception as e:
            logger.error(f"❌ Failed to translate precaution {i+1}: {str(e)}")
            translated_precautions.append(precaution)  # Fallback to English
    
    logger.info(f"✅ PRECAUTIONS TRANSLATION COMPLETE: {len(translated_precautions)} items")
    return translated_precautions

def get_somali_precautions_for_disease(disease_name):
    """
    Get Somali disease-specific precautions
    """
    try:
        # Map English disease names to Somali keys
        disease_mapping = {
            'diabetes': 'Sonkorowga',
            'malaria': 'Malaria', 
            'pneumonia': 'Burunkiito',
            'bronchitis': 'Burunkiito',
            'migraine': 'Migraine',
            'urinary tract infection': 'Infekshanka kaadi mareenka',
            'uti': 'Infekshanka kaadi mareenka',
            'typhoid': 'Typhoid',
            'fungal infection': 'Infekshanka fungal',
            'common cold': 'Qawowga caadiga ah',
            'cold': 'Qawowga caadiga ah',
            'flu': 'Qawowga caadiga ah'
        }
        
        disease_lower = disease_name.lower().strip()
        logger.info(f"🔍 Looking for Somali precautions for: {disease_name}")
        
        # Direct match
        if disease_lower in disease_mapping:
            somali_key = disease_mapping[disease_lower]
            if somali_key in disease_precautions:
                logger.info(f"✅ Found direct Somali precautions for: {disease_name} -> {somali_key}")
                return disease_precautions[somali_key]
        
        # Partial match
        for eng_key, somali_key in disease_mapping.items():
            if eng_key in disease_lower or disease_lower in eng_key:
                if somali_key in disease_precautions:
                    logger.info(f"✅ Found partial Somali precautions: {eng_key} -> {somali_key}")
                    return disease_precautions[somali_key]
        
        # Default Somali precautions
        logger.info(f"⚠️ No specific Somali precautions found for: {disease_name}, using default")
        return [
            "La tashii dhakhtar si aad u hesho daaweyn sax ah.",
            "Hel nasasho badan oo cab biyo badan.",
            "Raac talada dhakhtarkaaga oo qaado daawooyinka laguu qoro."
        ]
        
    except Exception as e:
        logger.error(f"❌ Error getting Somali precautions for {disease_name}: {str(e)}")
        return [
            "La tashii dhakhtar si aad u hesho daaweyn sax ah.",
            "Hel nasasho badan oo cab biyo badan.",
            "Raac talada dhakhtarkaaga oo qaado daawooyinka laguu qoro."
        ]

def get_precautions_for_disease(disease_name):
    """
    Get English precautions for a specific disease
    """
    logger.info(f"🔍 Getting English precautions for: {disease_name}")
    
    # Map disease names to English precautions
    disease_precautions_map = {
        'pneumonia': [
            "Take prescribed antibiotics or antiviral medications as directed by your doctor",
            "Get plenty of rest and avoid strenuous activities",
            "Drink plenty of fluids to stay hydrated and help loosen mucus",
            "Use a humidifier or breathe steam from a hot shower to ease breathing",
            "Avoid smoking and exposure to secondhand smoke",
            "Follow up with your healthcare provider as recommended"
        ],
        'malaria': [
            "Take antimalarial medications exactly as prescribed by your doctor",
            "Use mosquito nets while sleeping, especially during night hours",
            "Apply insect repellent containing DEET to exposed skin",
            "Wear long-sleeved clothing and long pants during evening and night",
            "Seek immediate medical attention if symptoms worsen",
            "Complete the full course of treatment even if you feel better"
        ],
        'diabetes': [
            "Monitor your blood sugar levels regularly as advised by your healthcare provider",
            "Follow a balanced diet and control carbohydrate intake",
            "Take prescribed medications (insulin or oral drugs) consistently",
            "Engage in regular physical activity as recommended by your doctor",
            "Check your feet daily for cuts, sores, or signs of infection",
            "Schedule regular check-ups for eye, kidney, and foot examinations"
        ],
        'common cold': [
            "Get adequate rest to help your body recover",
            "Stay well hydrated by drinking water, herbal teas, or warm broths",
            "Use a humidifier or inhale steam to relieve congestion",
            "Gargle with warm salt water to soothe a sore throat",
            "Wash hands frequently to prevent spreading the infection",
            "Avoid close contact with others to prevent transmission"
        ],
        'migraine': [
            "Take prescribed migraine medications at the first sign of symptoms",
            "Rest in a quiet, dark, and cool room during an attack",
            "Apply a cold compress to your forehead or temples",
            "Identify and avoid known migraine triggers",
            "Maintain regular sleep and eating schedules",
            "Stay hydrated and manage stress levels"
        ],
        'typhoid': [
            "Take prescribed antibiotics exactly as directed by your doctor",
            "Get plenty of rest and avoid physical exertion",
            "Stay well hydrated with clean, safe water",
            "Follow a bland diet as recommended by your healthcare provider",
            "Practice good hand hygiene to prevent spreading infection",
            "Complete the full course of treatment even if symptoms improve"
        ],
        'urinary tract infection': [
            "Take prescribed antibiotics exactly as directed",
            "Drink plenty of water to help flush out bacteria",
            "Avoid caffeine, alcohol, and spicy foods",
            "Use heating pads to relieve discomfort",
            "Practice good hygiene and urinate frequently",
            "Follow up with your healthcare provider as recommended"
        ],
        'fungal infection': [
            "Keep the affected area clean and dry",
            "Apply prescribed antifungal medications as directed",
            "Wear loose, breathable clothing",
            "Avoid sharing personal items like towels or clothing",
            "Change socks and underwear frequently",
            "Follow up with your healthcare provider if symptoms persist"
        ]
    }
    
    # Convert disease name to lowercase for matching
    disease_lower = disease_name.lower().strip()
    
    # Try exact match first
    if disease_lower in disease_precautions_map:
        logger.info(f"✅ Found exact match for English precautions: {disease_name}")
        return disease_precautions_map[disease_lower]
    
    # Try partial matching
    for key, precautions in disease_precautions_map.items():
        if key in disease_lower or disease_lower in key:
            logger.info(f"✅ Found partial match for English precautions: {disease_name} -> {key}")
            return precautions
    
    # Default English precautions if no match found
    logger.info(f"⚠️ No specific English precautions found for: {disease_name}, using default")
    return [
        "Consult a healthcare professional immediately for proper diagnosis and treatment",
        "Follow your doctor's prescribed treatment plan carefully",
        "Monitor your symptoms and seek medical attention if they worsen",
        "Take prescribed medications exactly as directed",
        "Get adequate rest and maintain proper nutrition",
        "Stay hydrated and avoid self-medication"
    ]

def create_model_vector(english_symptoms):
    """
    Create vector for model prediction using TF-IDF vectorizer
    """
    try:
        # Use TF-IDF vectorizer to transform symptoms text
        vector = vectorizer.transform([english_symptoms])
        logger.info(f"📊 Vector created with {vector.nnz} non-zero features")
        return vector
    except Exception as e:
        logger.error(f"❌ Error creating vector: {str(e)}")
        return vectorizer.transform(["medical symptoms"])

def translate_precautions(precautions, target_lang="so"):
    if target_lang == "en":
        return precautions

    translated = []
    for p in precautions:
        try:
            translator_instance = GoogleTranslator(source="auto", target=target_lang)
            # Check if the method is async
            import inspect
            if inspect.iscoroutinefunction(translator_instance.translate):
                import asyncio
                translated_text = asyncio.run(translator_instance.translate(p))
            else:
                translated_text = translator_instance.translate(p)
            translated.append(translated_text)
        except Exception as e:
            logger.error(f"Translation error: {e}")
            translated.append(p)
    return translated

def validate_symptoms_rule_based(symptoms_text, language='en'):
    """
    Rule-based validation for medical symptoms - works without OpenAI
    Validates against common medical symptoms for the 8 trained diseases
    """
    try:
        logger.info(f"🔍 Rule-based validation for: '{symptoms_text[:50]}...'")
        
        # Convert to lowercase for matching
        symptoms_lower = symptoms_text.lower()
        
        # Define medical symptom keywords for each language
        if language == 'som':
            # Somali medical symptom keywords
            medical_keywords = [
                # General symptoms
                'qandho', 'dhidid', 'xanuun', 'daal', 'qaraar', 'shuban',
                'madax', 'calool', 'jilib', 'xabad', 'sanka', 'indho',
                'cuna', 'kaadi', 'matag', 'neefsasho', 'qufac', 'hindhis',
                'dhawaaqa', 'fuuqbaxa', 'hargab', 'cuncun',
                # Specific symptoms from user input
                'madax xanuun', 'lalabbo', 'mataq', 'iftiin xanuun', 
                'aragti xasaasi', 'cod xanuun', 'dareen xasaasi', 
                'aragti lumo', 'blurry vision', 'indho ku wareegsan',
                'iftiin dhalaalaya', 'auras', 'wareer', 'xasaasiyad',
                'xasaasiyad culus', 'wareer', 'daal',
                # Additional common symptoms
                'qandho', 'dhidid', 'shuban', 'qaraar', 'hindhis',
                'fuuqbaxa', 'hargab', 'cuncun', 'kaadi', 'matag',
                # Disease-specific symptoms
                'sonkor', 'duuma', 'kaneeco', 'burunkii', 'infekshan',
                'haraad', 'saddex', 'shidaal', 'dabaylaha', 'xamaasad'
            ]
            
            # Non-medical keywords that should invalidate (Somali)
            non_medical_keywords = [
                'lacag', 'baabuur', 'guri', 'shaqo', 'cashar', 'cunto',
                'bixi', 'tag', 'keen', 'nabad', 'nabadgelyo', 'telefon',
                'internet', 'facebook', 'whatsapp', 'film', 'heeso'
            ]
        else:
            # English medical symptom keywords
            medical_keywords = [
                # General symptoms
                'pain', 'fever', 'headache', 'cough', 'fatigue', 'nausea',
                'vomiting', 'diarrhea', 'constipation', 'dizziness', 'weakness',
                'chest', 'stomach', 'throat', 'nose', 'eye', 'ear', 'back',
                'joint', 'muscle', 'breathing', 'breath', 'swelling', 'rash',
                'itch', 'burn', 'ache', 'sore', 'hurt', 'sick', 'ill', 'blood',
                'urine', 'bowel', 'appetite', 'sleep', 'tired', 'chills',
                # Additional common symptoms
                'feeling', 'experiencing', 'having', 'got', 'got a', 'have a',
                'suffering', 'suffering from', 'symptoms', 'symptom',
                'difficulty', 'trouble', 'problem', 'issues', 'condition',
                'discomfort', 'uncomfortable', 'sensitive', 'sensitivity',
                'pressure', 'tightness', 'heaviness', 'lightheaded', 'dizzy',
                'nauseous', 'vomiting', 'throwing up', 'upset stomach',
                'stomach ache', 'belly pain', 'abdominal', 'cramps',
                'runny nose', 'stuffy nose', 'congested', 'congestion',
                'sore throat', 'scratchy throat', 'hoarse', 'voice',
                'dry cough', 'wet cough', 'productive cough',
                'body aches', 'muscle aches', 'joint pain', 'stiffness',
                'hot', 'cold', 'sweating', 'sweats', 'night sweats',
                'loss of appetite', 'no appetite', 'hungry', 'thirsty',
                'dehydrated', 'dehydration', 'dry mouth', 'dry eyes',
                'blurred vision', 'blurry', 'vision', 'seeing',
                'hearing', 'ears', 'ringing', 'tinnitus',
                'numbness', 'tingling', 'pins and needles',
                'shortness of breath', 'breathing', 'wheezing',
                'chest tightness', 'chest pressure', 'heartburn',
                'acid reflux', 'indigestion', 'gas', 'bloating',
                'constipation', 'diarrhea', 'loose stools',
                'frequent urination', 'burning', 'urination',
                'rash', 'hives', 'itching', 'itchy', 'redness',
                'swelling', 'edema', 'fluid retention',
                'bruising', 'bleeding', 'cuts', 'wounds',
                'infection', 'infected', 'pus', 'drainage',
                # Disease-specific symptoms
                'diabetes', 'sugar', 'insulin', 'malaria', 'mosquito', 'bite',
                'pneumonia', 'lung', 'infection', 'bacteria', 'virus',
                'migraine', 'headache', 'cold', 'flu', 'runny', 'congestion',
                'urinary', 'tract', 'fungal', 'typhoid', 'temperature'
            ]
            
            # Non-medical keywords that should invalidate (English)
            non_medical_keywords = [
                'money', 'car', 'house', 'work', 'job', 'school', 'food',
                'phone', 'computer', 'internet', 'facebook', 'game', 'movie',
                'music', 'sport', 'weather', 'politics', 'news', 'hello',
                'goodbye', 'thanks', 'please', 'how are you', 'what time'
            ]
        
        # Count medical vs non-medical keywords
        medical_count = 0
        non_medical_count = 0
        
        # More sophisticated matching for Somali
        if language == 'som':
            # Check for exact matches first
            for keyword in medical_keywords:
                if keyword in symptoms_lower:
                    medical_count += 1
            
            # Check for partial matches and common Somali medical terms
            somali_medical_indicators = [
                'xanuun', 'daal', 'qandho', 'dhidid', 'wareer', 'mataq', 'lalabbo',
                'madax', 'indho', 'iftiin', 'aragti', 'cod', 'dareen', 'xasaasiyad',
                'xasaasi', 'dhalaalaya', 'lumo', 'wareegsan', 'culus', 'daran'
            ]
            
            for indicator in somali_medical_indicators:
                if indicator in symptoms_lower and indicator not in [kw for kw in medical_keywords if indicator in kw]:
                    medical_count += 1
        else:
            # English matching (original logic)
            for keyword in medical_keywords:
                if keyword in symptoms_lower:
                    medical_count += 1
        
        for keyword in non_medical_keywords:
            if keyword in symptoms_lower:
                non_medical_count += 1
        
        # Check for common non-medical patterns
        non_medical_patterns = [
            'hello', 'hi', 'how are you', 'good morning', 'good evening',
            'what is', 'how to', 'when is', 'where is', 'why is',
            'test', 'testing', '123', 'abc'
        ]
        
        pattern_matches = sum(1 for pattern in non_medical_patterns if pattern in symptoms_lower)
        
        # Validation logic
        text_length = len(symptoms_text.strip())
        
        # Too short
        if text_length < 3:
            return {
                'is_valid': False,
                'confidence': 0.9,
                'reason': 'Text too short to contain meaningful medical symptoms',
                'suggestions': ['fever', 'headache', 'cough', 'pain'] if language == 'en' else ['qandho', 'madax xanuun', 'dhidid', 'xanuun']
            }
        
        # Contains non-medical patterns
        if pattern_matches > 0:
            return {
                'is_valid': False,
                'confidence': 0.8,
                'reason': 'Text appears to be greeting or non-medical query',
                'suggestions': ['fever and cough', 'headache and nausea', 'stomach pain'] if language == 'en' else ['qandho iyo dhidid', 'madax xanuun', 'calool xanuun']
            }
        
        # Too many non-medical keywords
        if non_medical_count > medical_count:
            # Be more lenient for Somali - only reject if significantly more non-medical
            if language == 'som' and medical_count >= 1 and non_medical_count <= medical_count + 2:
                # Allow some non-medical content in Somali if we have medical symptoms
                pass
            else:
                return {
                    'is_valid': False,
                    'confidence': 0.7,
                    'reason': 'Text contains more non-medical content than medical symptoms',
                    'suggestions': ['describe your symptoms like: pain, fever, cough'] if language == 'en' else ['ku sharax calaamahaaga sida: xanuun, qandho, dhidid']
                }
        
        # No medical keywords found
        if medical_count == 0:
            # Special handling for Somali - check if text contains medical context
            if language == 'som':
                # Check for medical context indicators in Somali
                medical_context_indicators = [
                    'badanaa', 'hal dhinac', 'aragti xasaasi', 'dareen xasaasi',
                    'blurry vision', 'auras', 'culus marka', 'la socdo', 'la hadlo'
                ]
                context_matches = sum(1 for indicator in medical_context_indicators if indicator in symptoms_lower)
                
                if context_matches > 0:
                    return {
                        'is_valid': True,
                        'confidence': 0.7,
                        'reason': f'Found {context_matches} medical context indicators in Somali text',
                        'suggestions': []
                    }
            
            return {
                'is_valid': False,
                'confidence': 0.8,
                'reason': 'No recognizable medical symptoms found',
                'suggestions': ['fever', 'headache', 'cough', 'pain', 'nausea'] if language == 'en' else ['qandho', 'madax xanuun', 'dhidid', 'xanuun', 'shuban', 'lalabbo', 'mataq', 'wareer']
            }
        
        # Valid medical symptoms found
        confidence = min(0.9, 0.5 + (medical_count * 0.1))
        
        # Be more lenient for Somali language
        if language == 'som' and medical_count >= 1:
            confidence = max(confidence, 0.7)  # Minimum 70% confidence for Somali with at least 1 medical keyword
            
        return {
            'is_valid': True,
            'confidence': confidence,
            'reason': f'Found {medical_count} medical symptom keywords',
            'suggestions': []
        }
        
    except Exception as e:
        logger.error(f"❌ Rule-based validation error: {str(e)}")
        return {
            'is_valid': False,
            'confidence': 0.3,
            'reason': 'Validation error occurred',
            'suggestions': []
        }

def validate_symptoms_with_openai(symptoms_text, language='en'):
    """
    Enhanced OpenAI validation specifically for the 8 trained diseases
    
    """
    if not openai_client:
        logger.warning("⚠️ OpenAI not available, using rule-based validation only")
        return validate_symptoms_rule_based(symptoms_text, language)
    
    try:
        # Create a more specific prompt for the 8 diseases
        diseases_list = "malaria, typhoid, pneumonia, common cold, migraine, diabetes, urinary tract infection, fungal infection"
        
        if language == 'som':
            print(f"🔍 Somali validation: '{symptoms_text[:50]}...'")
            prompt = f"""
            You are a medical expert specializing in Somali language medical symptoms. Analyze this Somali text to determine if it contains valid medical symptoms that could indicate one of these diseases: {diseases_list}.

            Text: "{symptoms_text}"
            
            IMPORTANT: Somali medical symptoms include terms like:
            - madax xanuun (headache)
            - lalabbo (nausea)
            - mataq (vomiting)
            - iftiin xanuun (light sensitivity)
            - aragti xasaasi (sensitive vision)
            - cod xanuun (sound sensitivity)
            - dareen xasaasi (sensitive hearing)
            - aragti lumo (blurry vision)
            - indho ku wareegsan (eye pain)
            - iftiin dhalaalaya (auras)
            - wareer (dizziness)
            - xasaasiyad (sensitivity)
            - daal (pain)
            - qandho (fever)
            - dhidid (cough)
            
            Return true if the text contains ANY of these medical symptoms or similar medical terms in Somali.
            
            Respond with ONLY a JSON object:
            {{
                "is_valid": boolean,
                "confidence": float (0.0-1.0),
                "reason": "brief explanation",
                "suggestions": ["symptom1", "symptom2"]
            }}
            """
        else:
            prompt = f"""
            You are a medical expert. Analyze this text to determine if it contains valid medical symptoms that could indicate one of these diseases: {diseases_list}.

            Text: "{symptoms_text}"
            
            BE STRICT: Only return true if the text contains actual medical symptoms either in English or Somali. Reject greetings, non-medical text, random words, or irrelevant content.
            
            Respond with ONLY a JSON object:
            {{
                "is_valid": boolean,
                "confidence": float (0.0-1.0),
                "reason": "brief explanation",
                "suggestions": ["symptom1", "symptom2"]
            }}
            """
        
        logger.info(f"🔍 Enhanced OpenAI validation: '{symptoms_text[:50]}...'")
        
        # Make API call to OpenAI
        response = openai_client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a strict medical symptom validator. Only validate true medical symptoms. Reject any non-medical content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.0  # Make it more deterministic
        )
        
        # Parse the response
        response_text = response.choices[0].message.content.strip()
        logger.info(f"🤖 OpenAI response: {response_text}")
        
        # Try to parse JSON response
        import json
        try:
            validation_result = json.loads(response_text)
            
            # Ensure required fields exist
            if 'is_valid' not in validation_result:
                validation_result['is_valid'] = False  # Default to invalid for safety
            if 'confidence' not in validation_result:
                validation_result['confidence'] = 0.5
            if 'reason' not in validation_result:
                validation_result['reason'] = 'OpenAI validation completed'
            if 'suggestions' not in validation_result:
                validation_result['suggestions'] = []
            
            logger.info(f"✅ OpenAI validation result: {validation_result['is_valid']} (confidence: {validation_result['confidence']})")
            return validation_result
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse OpenAI JSON response: {str(e)}")
            # Fallback to rule-based validation
            logger.info("🔄 Falling back to rule-based validation")
            return validate_symptoms_rule_based(symptoms_text, language)
            
    except Exception as e:
        logger.error(f"❌ OpenAI validation error: {str(e)}")
        # Fallback to rule-based validation
        logger.info("🔄 Falling back to rule-based validation")
        return validate_symptoms_rule_based(symptoms_text, language)

def apply_somali_disease_rules(somali_symptoms, ensemble_predictions, ensemble_confidences):
    """
    Apply Somali disease rules to improve prediction accuracy for similar diseases
    """
    try:
        logger.info(f"🔍 DEBUG: Applying Somali disease rules to: '{somali_symptoms[:50]}...'")
        logger.info(f"🔍 DEBUG: Disease rules available: {bool(DISEASE_RULES)}")
        logger.info(f"🔍 DEBUG: Number of disease rules: {len(DISEASE_RULES) if DISEASE_RULES else 0}")
        
        if not DISEASE_RULES:
            logger.warning("⚠️ Disease rules not available, skipping Somali rule application")
            return ensemble_predictions, ensemble_confidences
        
        # Convert symptoms to lowercase for matching
        symptoms_lower = somali_symptoms.lower()
        logger.info(f"🔍 DEBUG: Symptoms (lowercase): '{symptoms_lower}'")
        
        # Track rule-based adjustments
        rule_adjustments = {}
        applied_rules = []
        disease_scores = {}
        
        logger.info(f"🔍 DEBUG: Starting disease rule analysis...")
        
        # Calculate scores for each disease based on Somali symptoms
        for disease, rules in DISEASE_RULES.items():
            logger.info(f"🔍 DEBUG: Analyzing disease: '{disease}'")
            
            boost_score = 0
            penalize_score = 0
            boost_matches = []
            penalize_matches = []
            
            # Check boost keywords with exact matching
            boost_keywords = rules.get('boost_keywords', [])
            logger.info(f"🔍 DEBUG: Boost keywords for '{disease}': {boost_keywords}")
            
            for keyword in boost_keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    boost_score += 1
                    boost_matches.append(keyword)
                    applied_rules.append(f"BOOST: '{keyword}' -> {disease}")
                    logger.info(f"✅ DEBUG: BOOST MATCH: '{keyword}' found in symptoms for '{disease}'")
                else:
                    logger.info(f"❌ DEBUG: No boost match for '{keyword}' in '{disease}'")
            
            # Check penalize keywords with exact matching
            penalize_keywords = rules.get('penalize_keywords', [])
            logger.info(f"🔍 DEBUG: Penalize keywords for '{disease}': {penalize_keywords}")
            
            for keyword in penalize_keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    penalize_score += 1
                    penalize_matches.append(keyword)
                    applied_rules.append(f"PENALIZE: '{keyword}' -> {disease}")
                    logger.info(f"❌ DEBUG: PENALIZE MATCH: '{keyword}' found in symptoms for '{disease}'")
                else:
                    logger.info(f"✅ DEBUG: No penalize match for '{keyword}' in '{disease}'")
            
            # Calculate net score (boost - penalize)
            net_score = boost_score - penalize_score
            logger.info(f"📊 DEBUG: Disease '{disease}' final score: boost={boost_score}, penalize={penalize_score}, net={net_score}")
            
            # Store scores for all diseases, even if net_score is 0
            disease_scores[disease] = {
                'boost_score': boost_score,
                'penalize_score': penalize_score,
                'net_score': net_score,
                'boost_matches': boost_matches,
                'penalize_matches': penalize_matches
            }
            
            if net_score != 0:
                rule_adjustments[disease] = net_score
                logger.info(f"📊 Disease '{disease}': boost={boost_score} ({boost_matches}), penalize={penalize_score} ({penalize_matches}), net={net_score}")
            else:
                logger.info(f"⚠️ DEBUG: No adjustments for '{disease}' (net_score=0)")
        
        logger.info(f"🔍 DEBUG: Rule adjustments calculated: {rule_adjustments}")
        logger.info(f"🔍 DEBUG: Applied rules: {applied_rules}")
        
        # Apply adjustments to ensemble predictions
        adjusted_predictions = ensemble_predictions.copy()
        adjusted_confidences = ensemble_confidences.copy()
        
        logger.info(f"🔍 DEBUG: Original ensemble confidences: {ensemble_confidences}")
        
        # NEW: Force diseases with strong keyword matches into the prediction
        forced_diseases = {}
        for disease, score_info in disease_scores.items():
            net_score = score_info['net_score']
            
            # If a disease has strong positive matches and isn't in ensemble, force it in
            if net_score > 0 and disease not in adjusted_confidences:
                # Force the disease into predictions with a base confidence
                base_confidence = 0.3 + (0.1 * net_score)  # Base 0.3 + 0.1 per positive match
                forced_diseases[disease] = base_confidence
                logger.info(f"🎯 FORCED '{disease}' into predictions: {base_confidence:.3f} (net_score={net_score})")
            
            # If a disease has strong negative matches and is in ensemble, heavily penalize it
            elif net_score < 0 and disease in adjusted_confidences:
                original_confidence = adjusted_confidences[disease]
                penalize_factor = 0.3 * abs(net_score)  # 30% per negative match
                new_confidence = max(0.0, original_confidence - penalize_factor)
                adjusted_confidences[disease] = new_confidence
                logger.info(f"🎯 HEAVILY PENALIZED '{disease}': {original_confidence:.3f} -> {new_confidence:.3f} (-{penalize_factor:.3f})")
        
        # Add forced diseases to adjusted confidences
        adjusted_confidences.update(forced_diseases)
        
        # Calculate adjustment factors based on disease scores for existing diseases
        for disease, score_info in disease_scores.items():
            if disease in adjusted_confidences and disease not in forced_diseases:
                original_confidence = adjusted_confidences[disease]
                net_score = score_info['net_score']
                
                logger.info(f"🔍 DEBUG: Adjusting '{disease}': original_confidence={original_confidence:.3f}, net_score={net_score}")
                
                # More sophisticated adjustment based on number of matches
                if net_score > 0:
                    # Boost confidence based on number of positive matches
                    boost_factor = 0.2 * net_score  # 20% per positive match (increased from 15%)
                    new_confidence = min(1.0, original_confidence + boost_factor)
                    logger.info(f"🎯 BOOSTED '{disease}': {original_confidence:.3f} -> {new_confidence:.3f} (+{boost_factor:.3f})")
                else:
                    # Penalize confidence based on number of negative matches
                    penalize_factor = 0.2 * abs(net_score)  # 20% per negative match (increased from 15%)
                    new_confidence = max(0.0, original_confidence - penalize_factor)
                    logger.info(f"🎯 PENALIZED '{disease}': {original_confidence:.3f} -> {new_confidence:.3f} (-{penalize_factor:.3f})")
                
                adjusted_confidences[disease] = new_confidence
            elif disease not in adjusted_confidences:
                logger.warning(f"⚠️ DEBUG: Disease '{disease}' not found in ensemble predictions")
        
        logger.info(f"🔍 DEBUG: Adjusted confidences: {adjusted_confidences}")
        
        # Find the best prediction after adjustments
        if adjusted_confidences:
            best_disease = max(adjusted_confidences, key=adjusted_confidences.get)
            best_confidence = adjusted_confidences[best_disease]
            
            # Check if the prediction changed due to Somali rules
            original_best = max(ensemble_confidences, key=ensemble_confidences.get) if ensemble_confidences else None
            original_confidence = ensemble_confidences.get(original_best, 0) if original_best else 0
            
            logger.info(f"🔍 DEBUG: Original best prediction: '{original_best}' ({original_confidence:.3f})")
            logger.info(f"🔍 DEBUG: New best prediction: '{best_disease}' ({best_confidence:.3f})")
            
            if original_best and best_disease != original_best:
                logger.info(f"🔄 Somali rules CHANGED prediction: '{original_best}' ({original_confidence:.3f}) -> '{best_disease}' ({best_confidence:.3f})")
            elif original_best:
                logger.info(f"✅ Somali rules CONFIRMED prediction: '{best_disease}' ({best_confidence:.3f})")
            
            logger.info(f"🏆 Final prediction after Somali rules: '{best_disease}' (confidence: {best_confidence:.3f})")
            logger.info(f"📝 Applied rules: {applied_rules}")
            
            # Return the best prediction and all adjusted confidences
            return {best_disease: best_confidence}, adjusted_confidences
        else:
            logger.warning("⚠️ No diseases found in ensemble predictions")
            return ensemble_predictions, ensemble_confidences
            
    except Exception as e:
        logger.error(f"❌ Error applying Somali disease rules: {str(e)}")
        return ensemble_predictions, ensemble_confidences

def pre_filter_diseases_by_somali_symptoms(somali_symptoms):
    """
    Pre-filter diseases based on Somali symptoms to improve prediction accuracy
    """
    try:
        logger.info(f"🔍 Pre-filtering diseases based on Somali symptoms: '{somali_symptoms[:50]}...'")
        
        if not DISEASE_RULES:
            logger.warning("⚠️ Disease rules not available, skipping pre-filtering")
            return None
        
        # Convert symptoms to lowercase for matching
        symptoms_lower = somali_symptoms.lower()
        
        # Calculate initial scores for each disease
        disease_scores = {}
        
        for disease, rules in DISEASE_RULES.items():
            boost_score = 0
            penalize_score = 0
            
            # Check boost keywords
            for keyword in rules.get('boost_keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    boost_score += 1
            
            # Check penalize keywords
            for keyword in rules.get('penalize_keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    penalize_score += 1
            
            # Calculate net score
            net_score = boost_score - penalize_score
            
            if net_score > 0:  # Only consider diseases with positive scores
                disease_scores[disease] = net_score
                logger.info(f"📊 Pre-filter: '{disease}' score = {net_score} (boost: {boost_score}, penalize: {penalize_score})")
        
        # Return top diseases based on scores
        if disease_scores:
            # Sort by score (highest first)
            sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
            top_diseases = [disease for disease, score in sorted_diseases if score > 0]
            
            logger.info(f"🎯 Pre-filtered diseases: {top_diseases}")
            return top_diseases
        else:
            logger.info("⚠️ No diseases matched Somali symptoms in pre-filtering")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error in pre-filtering diseases: {str(e)}")
        return None
  
  

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()
        lang_param = data.get('lang', 'auto')
        user_id = data.get('user_id', 'anonymous')
        
        logger.info(f"🚀 STARTING PREDICTION PIPELINE")
        logger.info(f"📝 Original symptoms: '{symptoms}'")
        logger.info(f"🌐 Language param: '{lang_param}'")
        logger.info(f"👤 User ID: '{user_id}'")
        logger.info(f"📊 Request data: {data}")

        # Validation
        if not symptoms or len(symptoms) < 5:
            return jsonify({
                'message': 'Please provide more detailed symptoms (at least 5 characters).',
                'type': 'error'
            }), 400

        # STEP 1: SELECT LANGUAGE
        detected_lang = detect_language_fixed(symptoms, lang_param)
        logger.info(f"🌐 SELECTED LANGUAGE: {detected_lang}")

        # STEP 2: ENHANCED SYMPTOM VALIDATION
        logger.info(f"🔍 STEP 2: Enhanced symptom validation")
        logger.info(f"🔍 Detected language: {detected_lang}")
        logger.info(f"🔍 Symptoms to validate: '{symptoms}'")
        
        # First try rule-based validation (always works)
        rule_validation = validate_symptoms_rule_based(symptoms, detected_lang)
        logger.info(f"📋 Rule-based validation: {rule_validation['is_valid']} (confidence: {rule_validation['confidence']:.2f})")
        logger.info(f"📋 Rule-based reason: {rule_validation['reason']}")
        
        # Then try OpenAI validation (if available)
        openai_validation = validate_symptoms_with_openai(symptoms, detected_lang)
        logger.info(f"🤖 OpenAI validation: {openai_validation['is_valid']} (confidence: {openai_validation['confidence']:.2f})")
        logger.info(f"🤖 OpenAI reason: {openai_validation['reason']}")
        
        # Combine both validations - be more lenient for Somali
        if detected_lang == 'som':
            # For Somali, accept if EITHER validation passes
            final_validation = {
                'is_valid': rule_validation['is_valid'] or openai_validation['is_valid'],
                'confidence': max(rule_validation['confidence'], openai_validation['confidence']),
                'reason': f"Rule-based: {rule_validation['is_valid']} ({rule_validation['confidence']:.2f}); OpenAI: {openai_validation['is_valid']} ({openai_validation['confidence']:.2f})",
                'suggestions': rule_validation['suggestions'] if rule_validation['suggestions'] else openai_validation['suggestions']
            }
        else:
            # For English, accept if EITHER validation passes (same as Somali)
            final_validation = {
                'is_valid': rule_validation['is_valid'] or openai_validation['is_valid'],
                'confidence': max(rule_validation['confidence'], openai_validation['confidence']),
                'reason': f"Rule-based: {rule_validation['is_valid']} ({rule_validation['confidence']:.2f}); OpenAI: {openai_validation['is_valid']} ({openai_validation['confidence']:.2f})",
                'suggestions': rule_validation['suggestions'] if rule_validation['suggestions'] else openai_validation['suggestions']
            }
        
        # If either validation fails, return error with suggestions
        if not final_validation['is_valid']:
            # Special fallback for Somali - check if it contains obvious medical terms
            if detected_lang == 'som':
                symptoms_lower = symptoms.lower()
                obvious_medical_terms = ['madax', 'xanuun', 'lalabbo', 'mataq', 'wareer', 'daal', 'qandho', 'dhidid']
                medical_term_count = sum(1 for term in obvious_medical_terms if term in symptoms_lower)
                
                if medical_term_count >= 2:  # If at least 2 obvious medical terms found
                    logger.info(f"🔍 Somali fallback: Found {medical_term_count} obvious medical terms, bypassing validation")
                    final_validation['is_valid'] = True
                    final_validation['confidence'] = 0.8
                    final_validation['reason'] = f"Fallback: Found {medical_term_count} obvious Somali medical terms"
                else:
                    suggestions_text = ""
                    if final_validation['suggestions']:
                        suggestions_text = f" Please provide valid medical symptoms such as: {', '.join(final_validation['suggestions'][:3])}"
                    
                    return jsonify({
                        'message': f'The provided text does not appear to contain valid medical symptoms. {final_validation["reason"]}{suggestions_text}',
                        'type': 'invalid_symptoms',
                        'validation_result': final_validation,
                        'rule_validation': rule_validation,
                        'openai_validation': openai_validation
                    }), 400
            else:
                # Special fallback for English - check if it contains obvious medical terms
                symptoms_lower = symptoms.lower()
                obvious_medical_terms = ['fever', 'headache', 'pain', 'cough', 'nausea', 'dizziness', 'fatigue', 'weakness', 'sore', 'ache', 'hurt', 'sick', 'ill']
                medical_term_count = sum(1 for term in obvious_medical_terms if term in symptoms_lower)
                
                logger.info(f"🔍 English fallback check: Found {medical_term_count} obvious medical terms in '{symptoms_lower}'")
                logger.info(f"🔍 English fallback check: Obvious terms found: {[term for term in obvious_medical_terms if term in symptoms_lower]}")
                
                if medical_term_count >= 1:  # If at least 1 obvious medical term found
                    logger.info(f"🔍 English fallback: Found {medical_term_count} obvious medical terms, bypassing validation")
                    final_validation['is_valid'] = True
                    final_validation['confidence'] = 0.8
                    final_validation['reason'] = f"Fallback: Found {medical_term_count} obvious English medical terms"
                else:
                    logger.info(f"🔍 English fallback: No obvious medical terms found, rejecting")
                    suggestions_text = ""
                    if final_validation['suggestions']:
                        suggestions_text = f" Please provide valid medical symptoms such as: {', '.join(final_validation['suggestions'][:3])}"
                    
                    return jsonify({
                        'message': f'The provided text does not appear to contain valid medical symptoms. {final_validation["reason"]}{suggestions_text}',
                        'type': 'invalid_symptoms',
                        'validation_result': final_validation,
                        'rule_validation': rule_validation,
                        'openai_validation': openai_validation
                    }), 400
        
        logger.info(f"✅ Enhanced symptom validation passed (combined confidence: {final_validation['confidence']:.2f})")

        # STEP 3: TRANSLATE SYMPTOMS TO ENGLISH
        if detected_lang == 'som':
            logger.info(f"🔄 TRANSLATING SYMPTOMS: Somali -> English")
            english_symptoms = translate_text_fixed(symptoms, 'som', 'en')
            logger.info(f"✅ TRANSLATED SYMPTOMS: '{english_symptoms[:100]}...'")
        else:
            english_symptoms = symptoms
            logger.info(f"📝 USING ENGLISH SYMPTOMS DIRECTLY")

        # STEP 4: ENSEMBLE MODEL PREDICTION
        try:
            symptoms_vector = create_model_vector(english_symptoms)
            logger.info(f"🔍 DEBUG: Created symptoms vector with shape: {symptoms_vector.shape}")
            
            # Use ensemble prediction with all available models and Somali disease rules
            somali_symptoms_for_rules = symptoms if detected_lang == 'som' else None
            
            logger.info(f"🔍 DEBUG: === ENSEMBLE PREDICTION WITH DISEASE RULES ===")
            logger.info(f"🔍 DEBUG: Detected language: {detected_lang}")
            logger.info(f"🔍 DEBUG: Original symptoms: '{symptoms}'")
            logger.info(f"🔍 DEBUG: English symptoms: '{english_symptoms}'")
            logger.info(f"🔍 DEBUG: Somali symptoms for rules: '{somali_symptoms_for_rules}'")
            logger.info(f"🔍 DEBUG: Disease rules available: {bool(DISEASE_RULES)}")
            logger.info(f"🔍 DEBUG: Available models: {list(models.keys())}")
            logger.info(f"🔍 DEBUG: Vectorizer vocabulary size: {len(vectorizer.vocabulary_)}")
            logger.info(f"🔍 DEBUG: Label encoder classes: {list(label_encoder.classes_)}")
            
            ensemble_result = ensemble_predict(
                symptoms_vector, 
                english_symptoms, 
                somali_symptoms=somali_symptoms_for_rules,
                detected_lang=detected_lang
            )
            prediction_english = ensemble_result['prediction']
            confidence = ensemble_result['confidence']
            
            logger.info(f"✅ ENSEMBLE PREDICTION: '{prediction_english}' (confidence: {confidence:.4f})")
            logger.info(f"📊 Used {ensemble_result['model_count']} models for prediction")
            if detected_lang == 'som':
                logger.info(f"🔍 Applied Somali disease rules for improved accuracy")
                logger.info(f"🔍 DEBUG: Final prediction after disease rules: '{prediction_english}'")

        except Exception as e:
            logger.error(f"❌ Ensemble prediction error: {str(e)}")
            logger.error(f"❌ Error details: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            return jsonify({
                'message': 'Error making prediction with the ensemble models.',
                'type': 'error',
                'error_details': str(e)
            }), 500

        # Check confidence threshold - increased for better accuracy
        if confidence < 0.30:
            return jsonify({
                'message': f'System confidence too low ({(confidence * 100):.0f}%). Please provide more specific medical symptoms.',
                'type': 'low_confidence',
                'confidence': float(confidence),
                'suggestions': ['fever', 'headache', 'cough', 'pain', 'nausea'] if detected_lang == 'en' else ['qandho', 'madax xanuun', 'dhidid', 'xanuun', 'shuban']
            }), 200

        # STEP 5: GET PRECAUTIONS BASED ON SELECTED LANGUAGE
        if detected_lang == 'som':
            # Get Somali precautions
            final_precautions = get_somali_precautions_for_disease(prediction_english)
            logger.info(f"✅ GOT SOMALI PRECAUTIONS: {len(final_precautions)} items")
        else:
            # Get English precautions
            final_precautions = get_precautions_for_disease(prediction_english)
            logger.info(f"✅ GOT ENGLISH PRECAUTIONS: {len(final_precautions)} items")

        # STEP 6: PREPARE RESPONSE DATA
        # Always keep disease prediction in English
        final_disease_name = prediction_english  # Always in English
        final_lang = detected_lang  # Keep track of original input language

        # STEP 7: LOG AND RETURN
        logger.info(f"Saving prediction to MongoDB for user_id: {user_id}")
        prediction_log_id = log_prediction(
            user_id, symptoms, final_disease_name, confidence, 
            final_lang, prediction_english, final_precautions
        )
        
        if prediction_log_id:
            logger.info(f"✅ Prediction saved with ID: {prediction_log_id}")
        else:
            logger.warning("⚠️ Prediction was not saved to database")

        # Format response to match chat interface expectations
        response_data = {
            'message': 'Ensemble prediction completed successfully.',
            'type': 'diagnosis',
            'disease': final_disease_name,  # Always in English
            'disease_english': prediction_english,  # English prediction from model
            'disease_somali': prediction_english,  # Keep disease name in English (no translation)
            'confidence': float(confidence),
            'precautions': final_precautions,  # In the selected language (English or Somali)
            'lang': final_lang,  # Original input language
            'prediction_id': prediction_log_id,
            'ensemble_info': {
                'model_count': ensemble_result['model_count'],
                'individual_predictions': ensemble_result['individual_predictions'],
                'individual_confidences': ensemble_result['individual_confidences'],
                'avg_confidence': float(ensemble_result['avg_confidence'])
            },
            'debug_info': {
                'detected_language': detected_lang,
                'original_disease': prediction_english,
                'precautions_count': len(final_precautions),
                'translation_info': {
                    'english_prediction': prediction_english,
                    'somali_translation': 'N/A',  # No disease translation
                    'translation_method': 'none'
                }
            }
        }

        logger.info(f"🎉 PIPELINE COMPLETE!")
        logger.info(f"   Final Disease: '{final_disease_name}' (always in English)")
        logger.info(f"   Final Language: '{final_lang}' (input language)")
        logger.info(f"   Precautions Count: {len(final_precautions)} (in {final_lang} language)")
        
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}", exc_info=True)
        return jsonify({
            'message': 'An internal server error occurred.',
            'type': 'error'
        }), 500

def log_prediction(user_id, original_symptoms, displayed_prediction, probability, displayed_lang, actual_prediction_en, precautions):
    try:
        # Create prediction document
        prediction_data = {
            'user_id': user_id,
            'symptoms_original': original_symptoms,
            'language_original': displayed_lang,
            'prediction_displayed': displayed_prediction,
            'prediction_actual_en': actual_prediction_en,
            'probability': float(probability),
            'precautions': precautions,
            'timestamp': datetime.utcnow(),
            'translation_method': 'google_translate_fixed',
            'saved_at': datetime.utcnow().isoformat()
        }
        
        # Insert into MongoDB with retry logic
        max_retries = 3
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                result = predictions_collection.insert_one(prediction_data)
                logger.info(f"✅ Prediction saved successfully with ID: {result.inserted_id}")
                return str(result.inserted_id)
            except Exception as e:
                retry_count += 1
                last_error = e
                logger.warning(f"MongoDB insertion attempt {retry_count} failed: {str(e)}")
                time.sleep(0.5)  # Wait before retrying
        
        # If we get here, all retries failed
        logger.error(f"❌ Failed to save prediction after {max_retries} attempts: {str(last_error)}")
        return None
    except Exception as e:
        logger.error(f"❌ Error logging prediction: {str(e)}")
        return None

@app.route('/test-translation-debug', methods=['POST'])
def test_translation_debug():
    """
    DEBUG endpoint to test translation step by step
    """
    try:
        data = request.get_json()
        text = data.get('text', 'Waxaan qabaa qandho iyo madax xanuun')
        
        result = {
            'original_text': text,
            'translator_available': translator is not None,
            'steps': []
        }
        
        if translator is None:
            result['error'] = 'Deep Translator not available'
            return jsonify(result), 503
        
        # Step 1: Language selection
        detected_lang = detect_language_fixed(text, 'auto')
        result['steps'].append({
            'step': 'language_selection',
            'detected': detected_lang,
            'success': True
        })
        
        # Step 2: Translate to English if Somali
        if detected_lang == 'som':
            english_translation = translate_text_fixed(text, 'som', 'en')
            result['steps'].append({
                'step': 'somali_to_english',
                'result': english_translation,
                'success': english_translation != text
            })
            
            # Step 3: Translate back to Somali
            back_to_somali = translate_text_fixed(english_translation, 'en', 'som')
            result['steps'].append({
                'step': 'english_to_somali',
                'result': back_to_somali,
                'success': back_to_somali != english_translation
            })
        
        # Step 4: Test precautions translation
        test_precautions = [
            "Take prescribed medications as directed",
            "Get plenty of rest",
            "Drink lots of water"
        ]
        
        if detected_lang == 'som':
            translated_precautions = translate_precautions_fixed(test_precautions, 'som')
            result['steps'].append({
                'step': 'precautions_translation',
                'original': test_precautions,
                'translated': translated_precautions,
                'success': len(translated_precautions) == len(test_precautions)
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-symptom-validation', methods=['POST'])
def test_symptom_validation():
    """
    DEBUG endpoint to test OpenAI symptom validation
    """
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', 'I have a headache and fever')
        language = data.get('language', 'en')
        
        result = {
            'original_symptoms': symptoms,
            'language': language,
            'openai_available': openai_client is not None,
            'validation_result': None
        }
        
        if not openai_client:
            result['error'] = 'OpenAI not available'
            return jsonify(result), 503
        
        # Test symptom validation
        validation_result = validate_symptoms_with_openai(symptoms, language)
        result['validation_result'] = validation_result
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-somali-disease-rules', methods=['POST'])
def test_somali_disease_rules():
    """
    DEBUG endpoint to test Somali disease rules application
    """
    try:
        data = request.get_json()
        somali_symptoms = data.get('symptoms', 'Waxaan qabaa qandho iyo madax xanuun')
        
        result = {
            'somali_symptoms': somali_symptoms,
            'disease_rules_available': bool(DISEASE_RULES),
            'applied_rules': [],
            'rule_adjustments': {}
        }
        
        if not DISEASE_RULES:
            result['error'] = 'Disease rules not available'
            return jsonify(result), 503
        
        # Test the disease rules application
        symptoms_lower = somali_symptoms.lower()
        
        for disease, rules in DISEASE_RULES.items():
            boost_score = 0
            penalize_score = 0
            
            # Check boost keywords
            for keyword in rules.get('boost_keywords', []):
                if keyword.lower() in symptoms_lower:
                    boost_score += 1
                    result['applied_rules'].append(f"BOOST: {keyword} -> {disease}")
            
            # Check penalize keywords
            for keyword in rules.get('penalize_keywords', []):
                if keyword.lower() in symptoms_lower:
                    penalize_score += 1
                    result['applied_rules'].append(f"PENALIZE: {keyword} -> {disease}")
            
            # Calculate net adjustment
            net_adjustment = boost_score - penalize_score
            
            if net_adjustment != 0:
                result['rule_adjustments'][disease] = {
                    'boost_score': boost_score,
                    'penalize_score': penalize_score,
                    'net_adjustment': net_adjustment,
                    'confidence_adjustment': 0.1 * net_adjustment
                }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-pre-filter-diseases', methods=['POST'])
def test_pre_filter_diseases():
    """
    DEBUG endpoint to test disease pre-filtering based on Somali symptoms
    """
    try:
        data = request.get_json()
        somali_symptoms = data.get('symptoms', 'Waxaan qabaa qandho iyo madax xanuun')
        
        result = {
            'somali_symptoms': somali_symptoms,
            'disease_rules_available': bool(DISEASE_RULES),
            'pre_filtered_diseases': None,
            'disease_scores': {}
        }
        
        if not DISEASE_RULES:
            result['error'] = 'Disease rules not available'
            return jsonify(result), 503
        
        # Test the pre-filtering
        pre_filtered = pre_filter_diseases_by_somali_symptoms(somali_symptoms)
        result['pre_filtered_diseases'] = pre_filtered
        
        # Also calculate detailed scores for each disease
        symptoms_lower = somali_symptoms.lower()
        
        for disease, rules in DISEASE_RULES.items():
            boost_score = 0
            penalize_score = 0
            boost_matches = []
            penalize_matches = []
            
            # Check boost keywords
            for keyword in rules.get('boost_keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    boost_score += 1
                    boost_matches.append(keyword)
            
            # Check penalize keywords
            for keyword in rules.get('penalize_keywords', []):
                keyword_lower = keyword.lower()
                if keyword_lower in symptoms_lower:
                    penalize_score += 1
                    penalize_matches.append(keyword)
            
            net_score = boost_score - penalize_score
            
            result['disease_scores'][disease] = {
                'boost_score': boost_score,
                'penalize_score': penalize_score,
                'net_score': net_score,
                'boost_matches': boost_matches,
                'penalize_matches': penalize_matches,
                'included_in_pre_filter': net_score > 0
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-specific-symptoms', methods=['POST'])
def test_specific_symptoms():
    """
    DEBUG endpoint to test specific symptoms with disease rules
    """
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', 'dhidid, qandho, shuban')
        
        result = {
            'symptoms': symptoms,
            'disease_rules_available': bool(DISEASE_RULES),
            'disease_analysis': {},
            'prediction_changes': {}
        }
        
        if not DISEASE_RULES:
            result['error'] = 'Disease rules not available'
            return jsonify(result), 503
        
        # Create mock ensemble predictions
        mock_predictions = {
            "malaria": 0.3,
            "migraine": 0.25,
            "typhoid": 0.2,
            "common cold": 0.25,
            "pneumonia": 0.2
        }
        
        # Apply Somali disease rules
        adjusted_predictions, adjusted_confidences = apply_somali_disease_rules(
            symptoms,
            mock_predictions,
            mock_predictions
        )
        
        # Analyze each disease
        symptoms_lower = symptoms.lower()
        
        for disease, rules in DISEASE_RULES.items():
            boost_matches = []
            penalize_matches = []
            
            # Check boost keywords
            for keyword in rules.get('boost_keywords', []):
                if keyword.lower() in symptoms_lower:
                    boost_matches.append(keyword)
            
            # Check penalize keywords
            for keyword in rules.get('penalize_keywords', []):
                if keyword.lower() in symptoms_lower:
                    penalize_matches.append(keyword)
            
            net_score = len(boost_matches) - len(penalize_matches)
            
            result['disease_analysis'][disease] = {
                'boost_matches': boost_matches,
                'penalize_matches': penalize_matches,
                'net_score': net_score,
                'original_confidence': mock_predictions.get(disease, 0),
                'adjusted_confidence': adjusted_confidences.get(disease, mock_predictions.get(disease, 0))
            }
        
        # Calculate prediction changes
        original_best = max(mock_predictions, key=mock_predictions.get)
        new_best = max(adjusted_confidences, key=adjusted_confidences.get)
        
        result['prediction_changes'] = {
            'original_best': original_best,
            'original_confidence': mock_predictions[original_best],
            'new_best': new_best,
            'new_confidence': adjusted_confidences[new_best],
            'prediction_changed': original_best != new_best
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-enhanced-validation', methods=['POST'])
def test_enhanced_validation():
    """
    DEBUG endpoint to test the new enhanced validation system
    """
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', 'hello how are you')
        language = data.get('language', 'en')
        
        result = {
            'symptoms': symptoms,
            'language': language,
            'validations': {}
        }
        
        # Test rule-based validation
        rule_validation = validate_symptoms_rule_based(symptoms, language)
        result['validations']['rule_based'] = rule_validation
        
        # Test OpenAI validation (if available)
        openai_validation = validate_symptoms_with_openai(symptoms, language)
        result['validations']['openai'] = openai_validation
        
        # Combined validation
        final_validation = {
            'is_valid': rule_validation['is_valid'] and openai_validation['is_valid'],
            'confidence': (rule_validation['confidence'] + openai_validation['confidence']) / 2,
            'reason': f"Rule-based: {rule_validation['reason']}; OpenAI: {openai_validation['reason']}",
            'suggestions': rule_validation['suggestions'] if rule_validation['suggestions'] else openai_validation['suggestions']
        }
        result['validations']['combined'] = final_validation
        
        # Test examples
        test_examples = [
            "hello how are you",
            "I have fever and headache", 
            "waxaan qabaa qandho iyo madax xanuun",
            "testing 123",
            "what time is it",
            "I feel pain in my chest and difficulty breathing",
            "Madax xanuun daran (badanaa hal dhinac ka ah), Lalabbo, Mataq, Iftiin xanuun (aragti xasaasi u ah iftiinka), Cod xanuun (dareen xasaasi u ah dhawaaqa), Aragti lumo (blurry vision), Indho ku wareegsan iftiin dhalaalaya (auras), Daal, Wareer, Xasaasiyad culus marka la socdo ama la hadlo"
        ]
        
        result['test_examples'] = {}
        for example in test_examples:
            example_rule = validate_symptoms_rule_based(example, language)
            
            # Add detailed analysis for Somali examples
            if language == 'som' or 'xanuun' in example.lower() or 'madax' in example.lower():
                example_lower = example.lower()
                analysis = {
                    'contains_madax': 'madax' in example_lower,
                    'contains_xanuun': 'xanuun' in example_lower,
                    'contains_lalabbo': 'lalabbo' in example_lower,
                    'contains_mataq': 'mataq' in example_lower,
                    'contains_wareer': 'wareer' in example_lower,
                    'contains_daal': 'daal' in example_lower,
                    'contains_aragti': 'aragti' in example_lower,
                    'contains_cod': 'cod' in example_lower,
                    'contains_dareen': 'dareen' in example_lower,
                    'contains_xasaasiyad': 'xasaasiyad' in example_lower,
                    'text_length': len(example)
                }
                result['test_examples'][example] = {
                    'rule_based': example_rule,
                    'would_pass': example_rule['is_valid'],
                    'analysis': analysis
                }
            else:
                result['test_examples'][example] = {
                    'rule_based': example_rule,
                    'would_pass': example_rule['is_valid']
                }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        # Check if MongoDB connection is available
        if 'predictions_collection' not in globals() or predictions_collection is None:
            logger.error("MongoDB connection not available for history retrieval")
            return jsonify({
                'error': 'Database connection not available',
                'status': 'error',
                'message': 'Unable to connect to the database. Please try again later.'
            }), 500
            
        # Get user predictions with sorting by timestamp
        user_predictions = list(predictions_collection.find({'user_id': user_id}).sort('timestamp', -1))
        
        # Process each prediction for JSON serialization and add additional fields
        for pred in user_predictions:
            if '_id' in pred:
                pred['_id'] = str(pred['_id'])
            if 'timestamp' in pred and isinstance(pred['timestamp'], datetime):
                pred['timestamp'] = pred['timestamp'].isoformat()
                # Add formatted date for display
                pred['formatted_date'] = pred['timestamp'].split('T')[0]
                
            # Ensure probability is properly formatted
            if 'probability' in pred:
                pred['probability'] = float(pred['probability'])
                pred['confidence_percentage'] = f"{pred['probability'] * 100:.2f}%"
                
            # Ensure precautions is always a list
            if 'precautions' not in pred or not isinstance(pred['precautions'], list):
                pred['precautions'] = []

        logger.info(f"Successfully retrieved {len(user_predictions)} prediction records for user {user_id}")
        return jsonify({
            'status': 'success',
            'count': len(user_predictions),
            'predictions': user_predictions
        }), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({
            'error': 'Could not retrieve prediction history',
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    try:
        data = request.get_json()
        prediction_id_str = data.get('prediction_id')
        user_id = data.get('user_id')
        helpful = data.get('helpful')

        if not prediction_id_str or not user_id or helpful is None:
            return jsonify({'error': 'Missing required fields'}), 400
        
        from bson import ObjectId
        try:
            prediction_obj_id = ObjectId(prediction_id_str) 
        except Exception:
            return jsonify({'error': 'Invalid prediction_id format'}), 400

        feedback_data = {
            'prediction_id': prediction_obj_id,
            'user_id': user_id,
            'helpful': bool(helpful),
            'timestamp': datetime.utcnow()
        }
        feedback_collection.insert_one(feedback_data)
        return jsonify({'message': 'Feedback received'}), 201
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        return jsonify({'error': 'Could not process feedback'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'deep_translator_available': translator is not None,
        'openai_available': openai_client is not None,
        'disease_rules_available': bool(DISEASE_RULES),
        'models_loaded': len(models),
        'model_names': list(models.keys()),
        'model_weights': model_weights,
        'vectorizer_loaded': vectorizer is not None,
        'label_encoder_loaded': label_encoder is not None,
        'feature_scaler_loaded': feature_scaler is not None,
        'tensorflow_available': TENSORFLOW_AVAILABLE
    }), 200

@app.route('/test-english-prediction', methods=['POST'])
def test_english_prediction():
    """
    Test endpoint to debug English prediction issues
    """
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', 'I have fever and headache')
        
        result = {
            'symptoms': symptoms,
            'models_loaded': len(models),
            'model_names': list(models.keys()),
            'vectorizer_loaded': vectorizer is not None,
            'label_encoder_loaded': label_encoder is not None,
            'feature_scaler_loaded': feature_scaler is not None,
            'prediction_steps': {}
        }
        
        # Step 1: Language detection
        detected_lang = detect_language_fixed(symptoms, 'auto')
        result['prediction_steps']['language_detection'] = {
            'detected_language': detected_lang,
            'success': True
        }
        
        # Step 2: Symptom validation
        rule_validation = validate_symptoms_rule_based(symptoms, detected_lang)
        result['prediction_steps']['symptom_validation'] = {
            'rule_based': rule_validation,
            'success': rule_validation['is_valid']
        }
        
        # Step 3: Create vector
        try:
            symptoms_vector = create_model_vector(symptoms)
            result['prediction_steps']['vector_creation'] = {
                'vector_shape': symptoms_vector.shape,
                'non_zero_features': symptoms_vector.nnz,
                'success': True
            }
        except Exception as e:
            result['prediction_steps']['vector_creation'] = {
                'error': str(e),
                'success': False
            }
            return jsonify(result), 500
        
        # Step 4: Test each model individually
        individual_predictions = {}
        for model_name, model in models.items():
            try:
                if model_name == 'deep_nn':
                    if feature_scaler is not None:
                        dense_vector = symptoms_vector.toarray()[0]
                        if len(dense_vector) < feature_scaler.n_features_in_:
                            padded_vector = np.zeros(feature_scaler.n_features_in_)
                            padded_vector[:len(dense_vector)] = dense_vector
                            feature_vector = padded_vector.reshape(1, -1)
                        elif len(dense_vector) > feature_scaler.n_features_in_:
                            feature_vector = dense_vector[:feature_scaler.n_features_in_].reshape(1, -1)
                        else:
                            feature_vector = dense_vector.reshape(1, -1)
                        
                        scaled_features = feature_scaler.transform(feature_vector)
                        prediction_probs = model.predict(scaled_features, verbose=0)
                        prediction_index = np.argmax(prediction_probs[0])
                        confidence = float(prediction_probs[0][prediction_index])
                        prediction = label_encoder.inverse_transform([prediction_index])[0]
                    else:
                        individual_predictions[model_name] = {
                            'error': 'Feature scaler not available',
                            'success': False
                        }
                        continue
                else:
                    prediction = model.predict(symptoms_vector)[0]
                    confidence_scores = model.predict_proba(symptoms_vector)[0]
                    confidence = confidence_scores.max()
                
                individual_predictions[model_name] = {
                    'prediction': prediction,
                    'confidence': float(confidence),
                    'success': True
                }
                
            except Exception as e:
                individual_predictions[model_name] = {
                    'error': str(e),
                    'success': False
                }
        
        result['prediction_steps']['individual_predictions'] = individual_predictions
        
        # Step 5: Test ensemble prediction
        try:
            ensemble_result = ensemble_predict(symptoms_vector, symptoms, None, detected_lang)
            result['prediction_steps']['ensemble_prediction'] = {
                'prediction': ensemble_result['prediction'],
                'confidence': float(ensemble_result['confidence']),
                'avg_confidence': float(ensemble_result['avg_confidence']),
                'model_count': ensemble_result['model_count'],
                'success': True
            }
        except Exception as e:
            result['prediction_steps']['ensemble_prediction'] = {
                'error': str(e),
                'success': False
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chat message endpoints
@app.route('/chat/message', methods=['POST'])
def save_chat_message():
    """Save a chat message to the database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('message') or not data.get('sender'):
            return jsonify({'error': 'Message and sender are required'}), 400
            
        # Create message document
        message_data = {
            'user_id': data.get('user_id', 'anonymous'),
            'message': data.get('message'),
            'sender': data.get('sender'),  # 'user' or 'ai'
            'prediction_id': data.get('prediction_id'),  # Only for AI messages
            'timestamp': datetime.utcnow(),
        }
        
        # Insert into database
        try:
            result = chat_messages_collection.insert_one(message_data)
            logger.info(f'✅ Chat message saved with ID: {result.inserted_id}')
            
            return jsonify({
                'success': True,
                'message_id': str(result.inserted_id)
            }), 201
        except Exception as e:
            logger.error(f'❌ Error inserting chat message: {str(e)}')
            return jsonify({'error': 'Database error'}), 500
        
    except Exception as e:
        logger.error(f'❌ Error saving chat message: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history for a user"""
    try:
        user_id = request.args.get('user_id', 'anonymous')
        limit = int(request.args.get('limit', 100))
        
        # Get messages for this user
        messages = list(chat_messages_collection.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for msg in messages:
            if '_id' in msg:
                msg['_id'] = str(msg['_id'])
            if 'timestamp' in msg and isinstance(msg['timestamp'], datetime):
                msg['timestamp'] = msg['timestamp'].isoformat()
                
        return jsonify(messages), 200
        
    except Exception as e:
        logger.error(f'❌ Error retrieving chat history: {str(e)}')
        return jsonify({'error': str(e)}), 500

def ensemble_predict(symptoms_vector, symptoms_text, somali_symptoms=None, detected_lang=None):
    """
    Make ensemble prediction using all available models with optional Somali disease rules
    """
    predictions = {}
    confidences = {}
    
    logger.info(f"🤖 ENSEMBLE PREDICTION: Using {len(models)} models")
    
    # Get predictions from each model
    for model_name, model in models.items():
        try:
            logger.info(f"🔍 DEBUG: Processing model: {model_name}")
            
            if model_name == 'deep_nn':
                # Deep neural network expects different input format
                # Convert TF-IDF vector to feature vector for deep NN
                if feature_scaler is not None:
                    logger.info(f"🔍 DEBUG: Deep NN - Feature scaler available, n_features_in_: {feature_scaler.n_features_in_}")
                    
                    # Convert sparse TF-IDF vector to dense array
                    dense_vector = symptoms_vector.toarray()[0]
                    logger.info(f"🔍 DEBUG: Deep NN - Dense vector length: {len(dense_vector)}")
                    
                    # Pad or truncate to match feature scaler dimensions
                    if len(dense_vector) < feature_scaler.n_features_in_:
                        # Pad with zeros if vector is too short
                        padded_vector = np.zeros(feature_scaler.n_features_in_)
                        padded_vector[:len(dense_vector)] = dense_vector
                        feature_vector = padded_vector.reshape(1, -1)
                        logger.info(f"🔍 DEBUG: Deep NN - Padded vector to {feature_scaler.n_features_in_} features")
                    elif len(dense_vector) > feature_scaler.n_features_in_:
                        # Truncate if vector is too long
                        feature_vector = dense_vector[:feature_scaler.n_features_in_].reshape(1, -1)
                        logger.info(f"🔍 DEBUG: Deep NN - Truncated vector to {feature_scaler.n_features_in_} features")
                    else:
                        feature_vector = dense_vector.reshape(1, -1)
                        logger.info(f"🔍 DEBUG: Deep NN - Vector length matches feature scaler")
                    
                    scaled_features = feature_scaler.transform(feature_vector)
                    logger.info(f"🔍 DEBUG: Deep NN - Scaled features shape: {scaled_features.shape}")
                    
                    prediction_probs = model.predict(scaled_features, verbose=0)
                    prediction_index = np.argmax(prediction_probs[0])
                    confidence = float(prediction_probs[0][prediction_index])
                    
                    # Get disease name from label encoder
                    prediction = label_encoder.inverse_transform([prediction_index])[0]
                    logger.info(f"🔍 DEBUG: Deep NN - Prediction index: {prediction_index}, Disease: {prediction}")
                else:
                    logger.warning("⚠️ Feature scaler not available for deep NN, skipping")
                    continue
                
            else:
                # Scikit-learn models
                logger.info(f"🔍 DEBUG: {model_name} - Using scikit-learn prediction")
                prediction = model.predict(symptoms_vector)[0]
                confidence_scores = model.predict_proba(symptoms_vector)[0]
                confidence = confidence_scores.max()
                logger.info(f"🔍 DEBUG: {model_name} - Prediction: {prediction}, Confidence scores shape: {confidence_scores.shape}")
            
            predictions[model_name] = prediction
            confidences[model_name] = confidence
            
            logger.info(f"   {model_name}: '{prediction}' (confidence: {confidence:.4f})")
            
        except Exception as e:
            logger.warning(f"⚠️ {model_name} prediction failed: {str(e)}")
            logger.warning(f"⚠️ {model_name} error details: {type(e).__name__}: {str(e)}")
            continue
    
    if not predictions:
        raise ValueError("All models failed to make predictions")
    
    # Weighted voting for final prediction
    weighted_votes = {}
    total_weight = 0
    
    for model_name, prediction in predictions.items():
        weight = model_weights[model_name]
        confidence = confidences[model_name]
        
        # Weight by both model weight and confidence
        effective_weight = weight * confidence
        
        if prediction not in weighted_votes:
            weighted_votes[prediction] = 0
        weighted_votes[prediction] += effective_weight
        total_weight += effective_weight
    
    # Get the prediction with highest weighted votes
    final_prediction = max(weighted_votes, key=weighted_votes.get)
    final_confidence = weighted_votes[final_prediction] / total_weight if total_weight > 0 else 0
    
    # Calculate ensemble confidence (average of all model confidences)
    avg_confidence = np.mean(list(confidences.values()))
    
    logger.info(f"🎯 ENSEMBLE RESULT: '{final_prediction}' (confidence: {final_confidence:.4f}, avg: {avg_confidence:.4f})")
    
    # Apply Somali disease rules if input is Somali
    if detected_lang == 'som' and somali_symptoms and DISEASE_RULES:
        logger.info(f"🔍 DEBUG: === SOMALI DISEASE RULES ACTIVATED ===")
        logger.info(f"🔍 DEBUG: Detected language: {detected_lang}")
        logger.info(f"🔍 DEBUG: Somali symptoms: '{somali_symptoms}'")
        logger.info(f"🔍 DEBUG: Disease rules available: {bool(DISEASE_RULES)}")
        logger.info(f"🔍 DEBUG: Number of disease rules: {len(DISEASE_RULES)}")
        logger.info(f"🔍 DEBUG: Applying Somali disease rules for better accuracy")
        
        # Create a mapping of predictions to confidences for rule application
        prediction_confidence_map = {}
        for prediction in set(predictions.values()):
            # Calculate average confidence for this prediction across all models
            pred_confidences = [confidences[model] for model, pred in predictions.items() if pred == prediction]
            if pred_confidences:
                prediction_confidence_map[prediction] = np.mean(pred_confidences)
        
        logger.info(f"🔍 DEBUG: Prediction confidence map before rules: {prediction_confidence_map}")
        
        # Apply Somali disease rules
        adjusted_predictions, adjusted_confidences = apply_somali_disease_rules(
            somali_symptoms, 
            prediction_confidence_map, 
            prediction_confidence_map
        )
        
        logger.info(f"🔍 DEBUG: Adjusted predictions after rules: {adjusted_predictions}")
        logger.info(f"🔍 DEBUG: Adjusted confidences after rules: {adjusted_confidences}")
        
        # Update final prediction if rules changed it
        if adjusted_predictions:
            new_final_prediction = list(adjusted_predictions.keys())[0]
            new_final_confidence = list(adjusted_predictions.values())[0]
            
            logger.info(f"🔍 DEBUG: Original final prediction: '{final_prediction}' ({final_confidence:.3f})")
            logger.info(f"🔍 DEBUG: New final prediction after rules: '{new_final_prediction}' ({new_final_confidence:.3f})")
            
            if new_final_prediction != final_prediction:
                logger.info(f"🔄 Somali rules CHANGED prediction: '{final_prediction}' -> '{new_final_prediction}'")
                final_prediction = new_final_prediction
                final_confidence = new_final_confidence
            else:
                logger.info(f"✅ Somali rules CONFIRMED prediction: '{final_prediction}'")
        else:
            logger.warning(f"⚠️ DEBUG: No adjusted predictions returned from disease rules")
    else:
        logger.info(f"🔍 DEBUG: === SOMALI DISEASE RULES NOT ACTIVATED ===")
        logger.info(f"🔍 DEBUG: Detected language: {detected_lang}")
        logger.info(f"🔍 DEBUG: Somali symptoms provided: {somali_symptoms is not None}")
        logger.info(f"🔍 DEBUG: Disease rules available: {bool(DISEASE_RULES)}")
        if detected_lang != 'som':
            logger.info(f"🔍 DEBUG: Skipping Somali rules - language is not Somali")
        elif not somali_symptoms:
            logger.info(f"🔍 DEBUG: Skipping Somali rules - no Somali symptoms provided")
        elif not DISEASE_RULES:
            logger.info(f"🔍 DEBUG: Skipping Somali rules - disease rules not available")
    
    return {
        'prediction': final_prediction,
        'confidence': final_confidence,
        'avg_confidence': avg_confidence,
        'individual_predictions': predictions,
        'individual_confidences': confidences,
        'model_count': len(predictions)
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Starting FIXED Translation Medical API on port {port}")
    logger.info(f"🌐 Translation: FIXED Deep Translator with proper Somali support")
    logger.info(f"🤖 Model: Disease prediction")
    logger.info(f"💊 Precautions: Translated to Somali")
    logger.info(f"💬 Chat messages: Stored in MongoDB")
    app.run(host='0.0.0.0', port=port, debug=True)
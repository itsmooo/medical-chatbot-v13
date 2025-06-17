from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from pymongo import MongoClient
from datetime import datetime
import logging
from dotenv import load_dotenv
import time

from deep_translator import GoogleTranslator


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Google Translator with better error handling
try:
    from googletrans import Translator
    translator = Translator()
    logger.info('✅ Google Translator initialized successfully')
    
    # Test the translator with Somali
    test_result = translator.translate('hello world', src='en', dest='so')
    logger.info(f'✅ Google Translator test successful: EN->SO = "{test_result.text}"')
    
    # Test reverse translation
    test_reverse = translator.translate('Waan ku salaamayaa', src='so', dest='en')
    logger.info(f'✅ Google Translator reverse test: SO->EN = "{test_reverse.text}"')
    
except Exception as e:
    logger.error(f'❌ Failed to initialize Google Translator: {str(e)}')
    translator = None

app = Flask(__name__)
CORS(app)

# MongoDB setup
try:
    client = MongoClient("mongodb://localhost:27017")
    db = client.DiseasePrediction
    predictions_collection = db.predictions
    feedback_collection = db.feedback
    logger.info('✅ MongoDB connected successfully')
except Exception as e:
    logger.error(f'❌ MongoDB connection failed: {str(e)}')

# Load the TRAINED MODEL
model_path = 'models/disease_predictor.pkl'
vectorizer_path = 'models/tfidf_vectorizer.pkl'
label_encoder_path = 'models/medical_label_encoder_20250609_203011.pkl'

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or not os.path.exists(label_encoder_path):
    logger.error(f"CRITICAL: Files not found. Searched paths: {model_path}, {vectorizer_path}, {label_encoder_path}")
    raise FileNotFoundError("Required model files not found")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(label_encoder_path)

logger.info(f"✅ Trained model loaded successfully. Vocabulary size: {len(vectorizer.vocabulary_)}")

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

def detect_language_fixed(text):
    """
    FIXED language detection with better logic
    """
    try:
        logger.info(f"🔍 DETECTING LANGUAGE for: '{text[:50]}...'")
        
        if translator is None:
            logger.warning("⚠️ Google Translator not available, defaulting to English")
            return 'en'
        
        # Use Google Translate's detect method
        detection = translator.detect(text)
        detected_lang = detection.lang
        confidence = detection.confidence
        
        logger.info(f"🔍 Google detected: '{detected_lang}' with confidence: {confidence}")
        
        # FIXED: Better language mapping
        if detected_lang == 'so':  # Somali
            logger.info("✅ CONFIRMED: Somali language detected")
            return 'som'
        elif detected_lang == 'en':  # English
            logger.info("✅ CONFIRMED: English language detected")
            return 'en'
        else:
            # For uncertain cases, check for Somali keywords
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
        logger.error(f"❌ Language detection failed: {str(e)}")
        return 'en'

def translate_text_fixed(text, source_lang, target_lang):
    """
    FIXED translation with proper language codes and debugging
    """
    try:
        logger.info(f"🔄 TRANSLATING: '{text[:50]}...' FROM {source_lang} TO {target_lang}")
        
        if translator is None:
            logger.warning("⚠️ Google Translator not available")
            return text
        
        # Skip if same language
        if source_lang == target_lang:
            logger.info("⚠️ Same language, skipping translation")
            return text
        
        # FIXED: Correct language codes for Google Translate
        google_source = 'so' if source_lang == 'som' else source_lang
        google_target = 'so' if target_lang == 'som' else target_lang
        
        logger.info(f"🔄 Using Google codes: {google_source} -> {google_target}")
        
        # Translate
        translation = translator.translate(text, src=google_source, dest=google_target)
        translated_text = translation.text
        
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
    FIXED precautions translation with better error handling
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

def get_precautions_for_disease(disease_name):
    """
    Get precautions for a specific disease
    """
    logger.info(f"🔍 Getting precautions for: {disease_name}")
    
    # Try exact match first
    if disease_name in DISEASE_PRECAUTIONS:
        precautions = DISEASE_PRECAUTIONS[disease_name]
        logger.info(f"✅ Found exact match: {len(precautions)} precautions")
        return precautions
    
    # Try partial match
    for disease_key in DISEASE_PRECAUTIONS.keys():
        if disease_key.lower() in disease_name.lower() or disease_name.lower() in disease_key.lower():
            precautions = DISEASE_PRECAUTIONS[disease_key]
            logger.info(f"✅ Found partial match ({disease_key}): {len(precautions)} precautions")
            return precautions
    
    # Use generic precautions
    logger.info(f"⚠️ Using generic precautions: {len(GENERIC_PRECAUTIONS)} items")
    return GENERIC_PRECAUTIONS

def create_model_vector(english_symptoms):
    """
    Create vector for model prediction
    """
    try:
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
            translated.append(GoogleTranslator(source="auto", target=target_lang).translate(p))
        except Exception as e:
            print(f"Translation error: {e}")
            translated.append(p)
    return translated
  
  

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

        # Validation
        if not symptoms or len(symptoms) < 5:
            return jsonify({
                'error': 'Please provide more detailed symptoms (at least 5 characters).',
                'is_unclear': True
            }), 400

        # STEP 1: DETECT LANGUAGE
        if lang_param in ['som', 'somali', 'so']:
            detected_lang = 'som'
            logger.info(f"🌐 FORCED LANGUAGE: Somali")
        elif lang_param in ['en', 'english', 'eng']:
            detected_lang = 'en'
            logger.info(f"🌐 FORCED LANGUAGE: English")
        else:
            detected_lang = detect_language_fixed(symptoms)
            logger.info(f"🌐 AUTO-DETECTED LANGUAGE: {detected_lang}")

        # STEP 2: TRANSLATE SYMPTOMS TO ENGLISH
        if detected_lang == 'som':
            logger.info(f"🔄 TRANSLATING SYMPTOMS: Somali -> English")
            english_symptoms = translate_text_fixed(symptoms, 'som', 'en')
            logger.info(f"✅ TRANSLATED SYMPTOMS: '{english_symptoms[:100]}...'")
        else:
            english_symptoms = symptoms
            logger.info(f"📝 USING ENGLISH SYMPTOMS DIRECTLY")

        # STEP 3: MODEL PREDICTION
        try:
            symptoms_vector = create_model_vector(english_symptoms)
            prediction_english = model.predict(symptoms_vector)[0]
            confidence_scores = model.predict_proba(symptoms_vector)[0]
            confidence = confidence_scores.max()
            
            logger.info(f"✅ MODEL PREDICTION: '{prediction_english}' (confidence: {confidence:.4f})")

        except Exception as e:
            logger.error(f"❌ Model prediction error: {str(e)}")
            return jsonify({
                'error': 'Error making prediction with the trained model.',
                'model_error': True
            }), 500

        # Check confidence threshold
        if confidence < 0.20:
            return jsonify({
                'error': f'System confidence too low ({(confidence * 100):.0f}%). Please provide more details.',
                'is_unclear': True,
                'confidence_too_low': True,
                'confidence': float(confidence)
            }), 200

        # STEP 4: GET PRECAUTIONS
        precautions_english = get_precautions_for_disease(prediction_english)
        logger.info(f"✅ GOT PRECAUTIONS: {len(precautions_english)} items")

        # STEP 5: TRANSLATE BACK TO ORIGINAL LANGUAGE
        if detected_lang == 'som':
            logger.info(f"🔄 TRANSLATING BACK TO SOMALI")
            
            # Translate disease name
            disease_name_somali = translate_text_fixed(prediction_english, 'en', 'som')
            logger.info(f"✅ DISEASE NAME TRANSLATED: '{disease_name_somali}'")
            
            # Translate precautions
            precautions_somali = translate_precautions_fixed(precautions_english, 'som')
            logger.info(f"✅ PRECAUTIONS TRANSLATED: {len(precautions_somali)} items")
            
            final_disease_name = disease_name_somali
            final_precautions = precautions_somali
            final_lang = 'som'
        else:
            final_disease_name = prediction_english
            final_precautions = precautions_english
            final_lang = 'en'

        # STEP 6: LOG AND RETURN
        prediction_log_id = log_prediction(
            user_id, symptoms, final_disease_name, confidence, 
            final_lang, prediction_english, final_precautions
        )
        
        predicted_precautions = translate_precautions(final_precautions, "so")

        response_data = {
            'disease': final_disease_name,
            'confidence': float(confidence),
            'precautions': final_precautions, 
            'lang': final_lang,
            'prediction_id': prediction_log_id, 
            'translated_text': predicted_precautions if detected_lang =="en" else final_precautions,
            'translation_method': 'google_translate_fixed',
            'debug_info': {
                'detected_language': detected_lang,
                'original_disease': prediction_english,
                'precautions_count': len(final_precautions)
            }
        }

        logger.info(f"🎉 PIPELINE COMPLETE!")
        logger.info(f"   Final Disease: '{final_disease_name}'")
        logger.info(f"   Final Language: '{final_lang}'")
        logger.info(f"   Precautions Count: {len(final_precautions)}")
        
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}", exc_info=True)
        return jsonify({'error': 'An internal server error occurred.'}), 500

def log_prediction(user_id, original_symptoms, displayed_prediction, probability, displayed_lang, actual_prediction_en, precautions):
    try:
        prediction_data = {
            'user_id': user_id,
            'symptoms_original': original_symptoms,
            'language_original': displayed_lang,
            'prediction_displayed': displayed_prediction,
            'prediction_actual_en': actual_prediction_en,
            'probability': float(probability),
            'precautions': precautions,
            'timestamp': datetime.utcnow(),
            'translation_method': 'google_translate_fixed'
        }
        result = predictions_collection.insert_one(prediction_data)
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error logging prediction: {str(e)}")
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
            result['error'] = 'Google Translator not available'
            return jsonify(result), 503
        
        # Step 1: Language detection
        detected_lang = detect_language_fixed(text)
        result['steps'].append({
            'step': 'language_detection',
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

@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        user_predictions = list(predictions_collection.find({'user_id': user_id}).sort('timestamp', -1))
        
        for pred in user_predictions:
            if '_id' in pred:
                pred['_id'] = str(pred['_id'])
            if 'timestamp' in pred and isinstance(pred['timestamp'], datetime):
                pred['timestamp'] = pred['timestamp'].isoformat()

        return jsonify(user_predictions), 200
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({'error': 'Could not retrieve prediction history'}), 500

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
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'translator_available': translator is not None,
        'model_loaded': model is not None,
        'vectorizer_loaded': vectorizer is not None
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Starting FIXED Translation Medical API on port {port}")
    logger.info(f"🌐 Translation: FIXED Google Translate with proper Somali support")
    logger.info(f"🤖 Model: Disease prediction")
    logger.info(f"💊 Precautions: Translated to Somali")
    app.run(host='0.0.0.0', port=port, debug=True)
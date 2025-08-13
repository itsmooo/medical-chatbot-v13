#!/usr/bin/env python3
"""
🧹 CLEANED UP BACKEND - Multiple Disease Prediction System
Optimized for performance with minimal model loading

Features:
- Only loads the 2 best performing models (87%+ accuracy)
- Simplified architecture for faster startup
- Clean, maintainable code structure
- Reduced memory usage
"""

import os
import sys
import json
import logging
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import pickle

# Try to import TensorFlow, but make it optional
TENSORFLOW_AVAILABLE = False
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
    logger = logging.getLogger(__name__)
    logger.info("✅ TensorFlow available")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("⚠️ TensorFlow not available - neural network models disabled")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://your-frontend-domain.com"])

# === GLOBAL PREPROCESSING COMPONENTS ===
symptoms_text_vectorizer = None
disease_label_encoder = None
feature_data_scaler = None
binary_feature_columns = None
disease_precautions_mapping = None

# === 🚀 DISEASE PREDICTION MODELS ===
disease_prediction_models = {}
model_ensemble_weights = {}
model_readable_names = {}

# Get the backend directory path for loading model files
backend_directory_path = os.path.dirname(os.path.abspath(__file__))

logger.info("🚀 Starting optimized model loading - Only best performing models!")

# 🥇 PRIMARY MODEL: Best performing ensemble model (87.68% accuracy)
try:
    disease_prediction_models['best_ensemble_model'] = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/ensemble_model.pkl'))
    model_ensemble_weights['best_ensemble_model'] = 0.60
    model_readable_names['best_ensemble_model'] = "Best Ensemble Model (87.68% Accuracy)"
    logger.info("✅ Best ensemble model loaded - 87.68% accuracy!")
except Exception as e:
    logger.warning(f"⚠️ Failed to load best ensemble model: {str(e)}")

# 🥈 SECONDARY MODEL: Best individual classifiers (87.91% accuracy)  
try:
    disease_prediction_models['best_individual_classifiers'] = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/individual_models.pkl'))
    model_ensemble_weights['best_individual_classifiers'] = 0.40
    model_readable_names['best_individual_classifiers'] = "Best Individual Classifiers (87.91% Accuracy)"
    logger.info("✅ Best individual classifiers loaded - 87.91% accuracy!")
except Exception as e:
    logger.warning(f"⚠️ Failed to load best individual classifiers: {str(e)}")

# Verify we have the essential disease prediction models
if not disease_prediction_models:
    logger.error("❌ Essential disease prediction models failed to load! Check fixed_v2 directory.")
    raise ValueError("Essential disease prediction models not found in disease_models/fixed_v2/")

# Neural network models removed for simplicity - using only ensemble models

# === LOAD TEXT PROCESSING AND DATA TRANSFORMATION COMPONENTS ===
try:
    # Load disease name encoder (converts predictions back to readable disease names)
    disease_label_encoder = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/label_encoder.pkl'))
    logger.info("✅ Loaded disease name encoder")
    
    # Load symptoms text vectorizer (converts symptom text to numerical features)
    symptoms_text_vectorizer = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/vectorizer.pkl'))
    logger.info("✅ Loaded symptoms text vectorizer")
    
    # Load feature data scaler (normalizes numerical features for models)
    feature_data_scaler = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/feature_scaler.pkl'))
    logger.info("✅ Loaded feature data scaler")
    
    # Load binary feature column names (defines which symptoms become features)
    binary_feature_columns = joblib.load(os.path.join(backend_directory_path, 'disease_models/fixed_v2/feature_columns.pkl'))
    logger.info(f"✅ Loaded binary feature columns: {len(binary_feature_columns)} symptom features")
    
    # Try to load disease treatment recommendations mapping
    try:
        disease_precautions_mapping = joblib.load(os.path.join(backend_directory_path, 'disease_models/precautions_mapping.pkl'))
        logger.info("✅ Loaded disease treatment recommendations")
    except:
        disease_precautions_mapping = {}
        logger.warning("⚠️ Disease treatment recommendations not found, using empty mapping")
    
except Exception as e:
    logger.error(f"❌ Failed to load text processing and data transformation components: {str(e)}")
    raise

# Verify we have at least one disease prediction model
if not disease_prediction_models:
    raise ValueError("❌ No disease prediction models could be loaded! Check model files.")

# Normalize ensemble weights so they sum to 1.0
total_ensemble_weight = sum(model_ensemble_weights.values())
if total_ensemble_weight > 0:
    for model_key in model_ensemble_weights:
        model_ensemble_weights[model_key] /= total_ensemble_weight
else:
    # Equal weights if no weights specified
    for model_key in model_ensemble_weights:
        model_ensemble_weights[model_key] = 1.0 / len(model_ensemble_weights)

logger.info(f"🎯 Loaded {len(disease_prediction_models)} disease prediction models:")
for model_key, ensemble_weight in model_ensemble_weights.items():
    readable_name = model_readable_names.get(model_key, model_key)
    logger.info(f"   - {model_key} ({readable_name}): weight {ensemble_weight:.2f}")

# === UTILITY FUNCTIONS ===

def convert_symptoms_text_to_numerical_features(user_symptoms_text):
    """Convert user's symptom description into numerical features for ML models"""
    if symptoms_text_vectorizer is None:
        logger.error("❌ Symptoms text vectorizer not loaded")
        return None
    
    try:
        numerical_symptom_features = symptoms_text_vectorizer.transform([user_symptoms_text])
        return numerical_symptom_features
    except Exception as e:
        logger.error(f"❌ Failed to convert symptoms text to features: {str(e)}")
        return None

def extract_individual_symptoms_from_user_input(user_input_text: str):
    """Extract individual symptom names from user's text input"""
    # Split user text by common delimiters to get individual symptoms
    individual_symptoms_list = []
    delimiters_to_split_on = [',', ';', '\n', ' and ', ' or ']
    
    # Replace all delimiters with a common separator
    text_with_common_delimiter = user_input_text
    for delimiter in delimiters_to_split_on:
        text_with_common_delimiter = text_with_common_delimiter.replace(delimiter, '|')
    
    # Split into individual symptom strings
    raw_symptom_strings = text_with_common_delimiter.split('|')
    
    # Clean and filter each symptom
    for raw_symptom in raw_symptom_strings:
        cleaned_symptom = raw_symptom.strip().lower()
        if cleaned_symptom and len(cleaned_symptom) > 2:  # Filter out very short strings
            individual_symptoms_list.append(cleaned_symptom)
    
    return individual_symptoms_list

def predict_disease_using_ensemble_of_models(numerical_symptom_features, original_user_input):
    """Predict disease by combining predictions from multiple ML models"""
    individual_model_predictions = {}
    individual_model_confidences = {}
    
    logger.info(f"🤖 ENSEMBLE DISEASE PREDICTION: Using {len(disease_prediction_models)} models")
    
    # Get disease predictions from each individual model
    for model_key, trained_model in disease_prediction_models.items():
        try:
            if model_ensemble_weights[model_key] == 0:  # Skip disabled models
                continue
                
            # Get disease prediction from this model
            predicted_disease = trained_model.predict(numerical_symptom_features)[0]
            prediction_confidence_scores = trained_model.predict_proba(numerical_symptom_features)[0]
            max_confidence = prediction_confidence_scores.max()
            
            individual_model_predictions[model_key] = predicted_disease
            individual_model_confidences[model_key] = max_confidence
            
            logger.info(f"🔍 {model_key}: {predicted_disease} (confidence: {max_confidence:.4f})")
            
        except Exception as e:
            logger.warning(f"⚠️ Model {model_key} failed: {str(e)}")
            continue
    
    if not individual_model_predictions:
        logger.error("❌ No models produced disease predictions")
        return {
            'final_disease_prediction': 'Unknown',
            'prediction_confidence': 0.0,
            'models_used_count': 0,
            'individual_predictions': {}
        }
    
    # Combine individual model predictions using weighted voting
    disease_vote_weights = {}
    total_ensemble_weight_used = 0
    
    for model_key, predicted_disease in individual_model_predictions.items():
        # Weight = model importance × confidence in this prediction
        vote_weight = model_ensemble_weights[model_key] * individual_model_confidences[model_key]
        
        if predicted_disease not in disease_vote_weights:
            disease_vote_weights[predicted_disease] = 0
        disease_vote_weights[predicted_disease] += vote_weight
        total_ensemble_weight_used += vote_weight
    
    # Choose the disease with the highest weighted vote
    if disease_vote_weights:
        final_predicted_disease = max(disease_vote_weights.items(), key=lambda x: x[1])[0]
        final_prediction_confidence = disease_vote_weights[final_predicted_disease] / total_ensemble_weight_used if total_ensemble_weight_used > 0 else 0
    else:
        # Fallback if no weighted voting possible
        final_predicted_disease = list(individual_model_predictions.values())[0]
        final_prediction_confidence = list(individual_model_confidences.values())[0]
    
    logger.info(f"✅ FINAL DISEASE PREDICTION: {final_predicted_disease} (confidence: {final_prediction_confidence:.4f})")
    
    return {
        'final_disease_prediction': final_predicted_disease,
        'prediction_confidence': float(final_prediction_confidence),
        'models_used_count': len(individual_model_predictions),
        'individual_predictions': individual_model_predictions
    }

# === API ROUTES ===

@app.route('/predict', methods=['POST'])
def predict_disease_from_user_symptoms():
    """API endpoint to predict disease from user's symptom description"""
    try:
        request_data = request.get_json()
        user_symptoms_text = request_data.get('symptoms', '').strip()
        
        if not user_symptoms_text:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        logger.info(f"🔍 Disease prediction request: '{user_symptoms_text}'")
        
        # Convert symptoms text to numerical features for ML models
        numerical_features = convert_symptoms_text_to_numerical_features(user_symptoms_text)
        if numerical_features is None:
            return jsonify({'error': 'Failed to process symptoms text'}), 500
        
        # Get disease prediction from ensemble of models
        prediction_result = predict_disease_using_ensemble_of_models(numerical_features, user_symptoms_text)
        
        # Get treatment recommendations for predicted disease
        predicted_disease_name = prediction_result['final_disease_prediction']
        treatment_recommendations = disease_precautions_mapping.get(predicted_disease_name, [])
        
        api_response = {
            'predicted_disease': predicted_disease_name,
            'confidence': prediction_result['prediction_confidence'],
            'treatment_recommendations': treatment_recommendations,
            'models_used': prediction_result['models_used_count'],
            'status': 'success'
        }
        
        logger.info(f"✅ Disease prediction successful: {predicted_disease_name} ({prediction_result['prediction_confidence']:.4f})")
        return jsonify(api_response)
        
    except Exception as e:
        logger.error(f"❌ Disease prediction failed: {str(e)}")
        return jsonify({'error': f'Disease prediction failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def check_backend_system_health():
    """API endpoint to check if the disease prediction system is working properly"""
    return jsonify({
        'system_status': 'healthy',
        'disease_models_loaded': len(disease_prediction_models),
        'loaded_model_names': list(disease_prediction_models.keys()),
        'symptoms_vectorizer_ready': symptoms_text_vectorizer is not None,
        'disease_encoder_ready': disease_label_encoder is not None,
        'feature_scaler_ready': feature_data_scaler is not None,
    })

@app.route('/models', methods=['GET'])
def get_disease_prediction_models_info():
    """API endpoint to get information about loaded disease prediction models"""
    models_info_list = []
    for model_key, ensemble_weight in model_ensemble_weights.items():
        models_info_list.append({
            'readable_name': model_readable_names.get(model_key, model_key),
            'internal_key': model_key,
            'ensemble_weight': ensemble_weight,
            'is_active': ensemble_weight > 0
        })
    
    return jsonify({
        'disease_prediction_models': models_info_list,
        'total_models_loaded': len(disease_prediction_models),
        'active_models_count': len([weight for weight in model_ensemble_weights.values() if weight > 0])
    })

if __name__ == '__main__':
    server_port = int(os.environ.get('PORT', 8000))
    logger.info(f"🚀 Starting disease prediction backend server on port {server_port}")
    logger.info(f"📊 Total disease prediction models loaded: {len(disease_prediction_models)}")
    logger.info(f"🎯 Active models in ensemble: {len([weight for weight in model_ensemble_weights.values() if weight > 0])}")
    
    app.run(host='0.0.0.0', port=server_port, debug=False)

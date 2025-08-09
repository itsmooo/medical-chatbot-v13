#!/usr/bin/env python3
"""
Test script to debug English prediction issues
"""

import requests
import json

def test_english_prediction():
    """Test English prediction with various symptoms"""
    
    # Test cases
    test_cases = [
        "I have fever and headache",
        "I am experiencing chest pain and difficulty breathing",
        "I have a cough and sore throat",
        "I feel dizzy and nauseous",
        "I have stomach pain and diarrhea"
    ]
    
    print("🔍 Testing English predictions...")
    print("=" * 50)
    
    for i, symptoms in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: '{symptoms}'")
        
        try:
            # Test the prediction endpoint
            response = requests.post(
                'http://localhost:5000/predict',
                json={
                    'symptoms': symptoms,
                    'lang': 'en',
                    'user_id': 'test_user'
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS:")
                print(f"   Disease: {result.get('disease', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
                print(f"   Type: {result.get('type', 'N/A')}")
                print(f"   Precautions count: {len(result.get('precautions', []))}")
            else:
                print(f"❌ ERROR ({response.status_code}):")
                error_data = response.json()
                print(f"   Message: {error_data.get('message', 'Unknown error')}")
                print(f"   Type: {error_data.get('type', 'N/A')}")
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🔍 Testing health endpoint...")
    
    try:
        health_response = requests.get('http://localhost:5000/health')
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ Health check successful:")
            print(f"   Models loaded: {health_data.get('models_loaded', 0)}")
            print(f"   Model names: {health_data.get('model_names', [])}")
            print(f"   Vectorizer loaded: {health_data.get('vectorizer_loaded', False)}")
            print(f"   Label encoder loaded: {health_data.get('label_encoder_loaded', False)}")
            print(f"   Feature scaler loaded: {health_data.get('feature_scaler_loaded', False)}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Health check exception: {str(e)}")

def test_debug_endpoint():
    """Test the debug endpoint"""
    
    print("\n🔍 Testing debug endpoint...")
    
    try:
        debug_response = requests.post(
            'http://localhost:5000/test-english-prediction',
            json={'symptoms': 'I have fever and headache'},
            headers={'Content-Type': 'application/json'}
        )
        
        if debug_response.status_code == 200:
            debug_data = debug_response.json()
            print("✅ Debug test successful:")
            print(f"   Models loaded: {debug_data.get('models_loaded', 0)}")
            print(f"   Model names: {debug_data.get('model_names', [])}")
            
            steps = debug_data.get('prediction_steps', {})
            
            # Language detection
            lang_detection = steps.get('language_detection', {})
            print(f"   Language detected: {lang_detection.get('detected_language', 'N/A')}")
            
            # Symptom validation
            validation = steps.get('symptom_validation', {})
            rule_based = validation.get('rule_based', {})
            print(f"   Validation passed: {validation.get('success', False)}")
            print(f"   Validation confidence: {rule_based.get('confidence', 0):.2f}")
            
            # Vector creation
            vector_creation = steps.get('vector_creation', {})
            print(f"   Vector created: {vector_creation.get('success', False)}")
            if vector_creation.get('success'):
                print(f"   Vector shape: {vector_creation.get('vector_shape', 'N/A')}")
                print(f"   Non-zero features: {vector_creation.get('non_zero_features', 0)}")
            
            # Individual predictions
            individual_predictions = steps.get('individual_predictions', {})
            print(f"   Individual predictions:")
            for model_name, pred_data in individual_predictions.items():
                if pred_data.get('success'):
                    print(f"     {model_name}: {pred_data.get('prediction', 'N/A')} ({pred_data.get('confidence', 0):.2f})")
                else:
                    print(f"     {model_name}: ERROR - {pred_data.get('error', 'Unknown error')}")
            
            # Ensemble prediction
            ensemble = steps.get('ensemble_prediction', {})
            if ensemble.get('success'):
                print(f"   Ensemble prediction: {ensemble.get('prediction', 'N/A')} ({ensemble.get('confidence', 0):.2f})")
            else:
                print(f"   Ensemble prediction: ERROR - {ensemble.get('error', 'Unknown error')}")
                
        else:
            print(f"❌ Debug test failed: {debug_response.status_code}")
            print(f"   Response: {debug_response.text}")
            
    except Exception as e:
        print(f"❌ Debug test exception: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting English prediction tests...")
    
    # Test health endpoint first
    test_english_prediction()
    
    # Test debug endpoint
    test_debug_endpoint()
    
    print("\n✅ Tests completed!") 
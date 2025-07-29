#!/usr/bin/env python3
"""
Test the actual ensemble prediction with real models
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_ensemble_prediction():
    """Test the actual ensemble prediction with real models"""
    
    # Import the functions
    from app import ensemble_predict, create_model_vector, DISEASE_RULES
    
    print("🔍 TESTING ACTUAL ENSEMBLE PREDICTION")
    print("=" * 50)
    
    # Test with the specific symptoms
    test_symptoms = "dhidid, qandho, shuban"
    
    print(f"🔍 Testing symptoms: '{test_symptoms}'")
    
    try:
        # Create vector for the symptoms
        symptoms_vector = create_model_vector(test_symptoms)
        print(f"✅ Vector created successfully")
        
        # Test ensemble prediction WITHOUT disease rules (English)
        print(f"\n🔍 Testing ensemble prediction (English mode):")
        result_english = ensemble_predict(
            symptoms_vector, 
            test_symptoms, 
            somali_symptoms=None,
            detected_lang='en'
        )
        
        print(f"🔍 English prediction result:")
        print(f"   Prediction: {result_english['prediction']}")
        print(f"   Confidence: {result_english['confidence']:.4f}")
        print(f"   Individual predictions: {result_english['individual_predictions']}")
        print(f"   Individual confidences: {result_english['individual_confidences']}")
        
        # Test ensemble prediction WITH disease rules (Somali)
        print(f"\n🔍 Testing ensemble prediction (Somali mode):")
        result_somali = ensemble_predict(
            symptoms_vector, 
            test_symptoms, 
            somali_symptoms=test_symptoms,
            detected_lang='som'
        )
        
        print(f"🔍 Somali prediction result:")
        print(f"   Prediction: {result_somali['prediction']}")
        print(f"   Confidence: {result_somali['confidence']:.4f}")
        print(f"   Individual predictions: {result_somali['individual_predictions']}")
        print(f"   Individual confidences: {result_somali['individual_confidences']}")
        
        # Compare results
        print(f"\n🔍 COMPARISON:")
        print(f"   English mode prediction: '{result_english['prediction']}' ({result_english['confidence']:.4f})")
        print(f"   Somali mode prediction: '{result_somali['prediction']}' ({result_somali['confidence']:.4f})")
        
        if result_english['prediction'] != result_somali['prediction']:
            print(f"✅ Disease rules CHANGED the prediction!")
        else:
            print(f"⚠️ Disease rules did NOT change the prediction")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ensemble_prediction()
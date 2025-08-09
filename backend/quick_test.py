#!/usr/bin/env python3
"""
Quick test script to verify English prediction fixes
"""

import requests
import json

def test_english_prediction():
    """Test English prediction with simple symptoms"""
    
    test_symptoms = "I have fever and headache"
    
    print(f"🔍 Testing English prediction with: '{test_symptoms}'")
    
    try:
        response = requests.post(
            'http://localhost:5000/predict',
            json={
                'symptoms': test_symptoms,
                'lang': 'auto',
                'user_id': 'test_user'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"   Disease: {result.get('disease', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            print(f"   Type: {result.get('type', 'N/A')}")
            print(f"   Precautions count: {len(result.get('precautions', []))}")
        else:
            print("❌ ERROR!")
            error_data = response.json()
            print(f"   Message: {error_data.get('message', 'Unknown error')}")
            print(f"   Type: {error_data.get('type', 'N/A')}")
            if 'validation_result' in error_data:
                print(f"   Validation result: {error_data['validation_result']}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_english_prediction() 
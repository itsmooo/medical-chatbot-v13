#!/usr/bin/env python3
"""
Test script to verify language-specific precautions
"""

import requests
import json

def test_language_precautions():
    """Test that precautions are returned in the correct language"""
    
    test_cases = [
        {
            'symptoms': 'I have fever and headache',
            'lang': 'en',
            'expected_language': 'English'
        },
        {
            'symptoms': 'Waxaan qabaa qandho iyo madax xanuun',
            'lang': 'so',
            'expected_language': 'Somali'
        }
    ]
    
    print("🔍 Testing language-specific precautions...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"   Symptoms: '{test_case['symptoms']}'")
        print(f"   Language: {test_case['lang']}")
        print(f"   Expected: {test_case['expected_language']} precautions")
        
        try:
            response = requests.post(
                'http://localhost:5000/predict',
                json={
                    'symptoms': test_case['symptoms'],
                    'lang': test_case['lang'],
                    'user_id': 'test_user'
                },
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS!")
                print(f"   Disease: {result.get('disease', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
                print(f"   Language: {result.get('lang', 'N/A')}")
                print(f"   Precautions count: {len(result.get('precautions', []))}")
                
                # Show first few precautions
                precautions = result.get('precautions', [])
                if precautions:
                    print(f"   First 2 precautions:")
                    for j, precaution in enumerate(precautions[:2], 1):
                        print(f"     {j}. {precaution}")
                
                # Check if precautions are in the right language
                if test_case['lang'] == 'en':
                    # Check for English words
                    english_indicators = ['take', 'get', 'drink', 'use', 'avoid', 'follow']
                    has_english = any(any(indicator in prec.lower() for indicator in english_indicators) 
                                    for prec in precautions)
                    print(f"   English indicators found: {has_english}")
                else:
                    # Check for Somali words
                    somali_indicators = ['la', 'ka', 'oo', 'iyo', 'wax', 'qabaa']
                    has_somali = any(any(indicator in prec.lower() for indicator in somali_indicators) 
                                   for prec in precautions)
                    print(f"   Somali indicators found: {has_somali}")
                    
            else:
                print(f"   ❌ ERROR!")
                error_data = response.json()
                print(f"   Message: {error_data.get('message', 'Unknown error')}")
                print(f"   Type: {error_data.get('type', 'N/A')}")
                
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    test_language_precautions() 
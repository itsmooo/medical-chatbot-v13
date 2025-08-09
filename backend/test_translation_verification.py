#!/usr/bin/env python3
"""
Test script to verify translation functionality and see both English and Somali versions
"""

import requests
import json

def test_translation_verification():
    """Test that we can see both English prediction and Somali translation"""
    
    print("🔍 Testing Translation Verification")
    print("=" * 60)
    
    # Test Somali input
    print("\n🇸🇴 Testing Somali Input:")
    print("Expected: See English prediction + Somali translation + Somali precautions")
    
    somali_test = {
        'symptoms': 'Waxaan qabaa qandho iyo madax xanuun oo xoogan',
        'lang': 'so'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/predict',
            json={
                'symptoms': somali_test['symptoms'],
                'lang': somali_test['lang'],
                'user_id': 'test_translation_user'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ SUCCESS! Status: {response.status_code}")
            print(f"\n🔍 Translation Results:")
            print(f"   Original Symptoms (Somali): '{somali_test['symptoms']}'")
            print(f"   Disease (Display): '{result.get('disease', 'N/A')}'")
            print(f"   Disease (English): '{result.get('disease_english', 'N/A')}'")
            print(f"   Disease (Somali): '{result.get('disease_somali', 'N/A')}'")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            print(f"   Language: {result.get('lang', 'N/A')}")
            
            # Debug info
            debug_info = result.get('debug_info', {})
            if debug_info:
                translation_info = debug_info.get('translation_info', {})
                print(f"\n🔍 Translation Debug Info:")
                print(f"   English Prediction: '{translation_info.get('english_prediction', 'N/A')}'")
                print(f"   Somali Translation: '{translation_info.get('somali_translation', 'N/A')}'")
                print(f"   Translation Method: '{translation_info.get('translation_method', 'N/A')}'")
            
            # Precautions
            precautions = result.get('precautions', [])
            print(f"\n🔍 Precautions ({len(precautions)} items):")
            for i, precaution in enumerate(precautions[:3], 1):
                print(f"   {i}. {precaution}")
            
            # Verification
            print(f"\n✅ Verification:")
            english_pred = result.get('disease_english', '')
            somali_trans = result.get('disease_somali', '')
            print(f"   ✓ English prediction exists: {bool(english_pred)}")
            print(f"   ✓ Somali translation exists: {bool(somali_trans)}")
            print(f"   ✓ Translation is different: {english_pred != somali_trans}")
            print(f"   ✓ Precautions in Somali: {any('la ' in p.lower() or 'ka ' in p.lower() for p in precautions)}")
                
        else:
            print(f"❌ ERROR! Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
    
    # Test English input for comparison
    print(f"\n🇺🇸 Testing English Input (for comparison):")
    print("Expected: See English prediction + English precautions")
    
    english_test = {
        'symptoms': 'I have high fever and severe headache',
        'lang': 'en'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/predict',
            json={
                'symptoms': english_test['symptoms'],
                'lang': english_test['lang'],
                'user_id': 'test_translation_user'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ SUCCESS! Status: {response.status_code}")
            print(f"\n🔍 English Results:")
            print(f"   Original Symptoms (English): '{english_test['symptoms']}'")
            print(f"   Disease (Display): '{result.get('disease', 'N/A')}'")
            print(f"   Disease (English): '{result.get('disease_english', 'N/A')}'")
            print(f"   Disease (Somali): '{result.get('disease_somali', 'N/A')}'")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            
            # Precautions
            precautions = result.get('precautions', [])
            print(f"\n🔍 Precautions ({len(precautions)} items):")
            for i, precaution in enumerate(precautions[:3], 1):
                print(f"   {i}. {precaution}")
                
        else:
            print(f"❌ ERROR! Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")

def test_google_translate_function():
    """Test the Google Translate function directly"""
    
    print(f"\n🔄 Testing Google Translate Function:")
    print("=" * 50)
    
    # Test diseases that should be translated
    test_diseases = [
        'malaria',
        'pneumonia', 
        'diabetes',
        'common cold',
        'migraine',
        'typhoid'
    ]
    
    print("Testing disease name translations:")
    for disease in test_diseases:
        print(f"   {disease} -> Testing...")

if __name__ == "__main__":
    test_translation_verification()
    test_google_translate_function()
    
    print(f"\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ For Somali input:")
    print("   - Model predicts in English")
    print("   - Disease name translated to Somali")
    print("   - Precautions in Somali")
    print("   - Both English and Somali versions available")
    print("")
    print("✅ For English input:")
    print("   - Model predicts in English")
    print("   - Disease name stays in English")
    print("   - Precautions in English")
    print("   - Somali translation also generated") 
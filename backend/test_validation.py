#!/usr/bin/env python3
"""
Test script to debug validation issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import validate_symptoms_rule_based, validate_symptoms_with_openai

def test_validation():
    """Test validation with various English symptoms"""
    
    test_cases = [
        "I have fever and headache",
        "I am experiencing chest pain and difficulty breathing",
        "I have a cough and sore throat",
        "I feel dizzy and nauseous",
        "I have stomach pain and diarrhea",
        "I have a headache",
        "I am feeling sick",
        "I have pain in my chest",
        "I am experiencing symptoms",
        "I have a cold",
        "I feel unwell",
        "I have been feeling ill",
        "I am suffering from fever",
        "I have got a headache",
        "I am having trouble breathing"
    ]
    
    print("🔍 Testing English symptom validation...")
    print("=" * 60)
    
    for i, symptoms in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: '{symptoms}'")
        
        # Test rule-based validation
        rule_result = validate_symptoms_rule_based(symptoms, 'en')
        print(f"   Rule-based: {rule_result['is_valid']} (confidence: {rule_result['confidence']:.2f})")
        print(f"   Reason: {rule_result['reason']}")
        
        # Test OpenAI validation (if available)
        try:
            openai_result = validate_symptoms_with_openai(symptoms, 'en')
            print(f"   OpenAI: {openai_result['is_valid']} (confidence: {openai_result['confidence']:.2f})")
            print(f"   Reason: {openai_result['reason']}")
        except Exception as e:
            print(f"   OpenAI: Error - {str(e)}")
        
        # Combined validation
        combined_valid = rule_result['is_valid'] or (openai_result['is_valid'] if 'openai_result' in locals() else False)
        print(f"   Combined: {'✅ VALID' if combined_valid else '❌ INVALID'}")
        
        if not combined_valid:
            print(f"   ❌ This would be rejected!")
        else:
            print(f"   ✅ This would be accepted!")

if __name__ == "__main__":
    test_validation() 
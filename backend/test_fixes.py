#!/usr/bin/env python3
"""
Test script to verify disease prediction fixes
Tests migraine and UTI symptoms specifically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import validate_symptoms_rule_based, apply_somali_disease_rules
import json

def test_migraine_symptoms():
    """Test migraine symptom validation and prediction"""
    print("🧪 Testing Migraine Symptoms...")
    
    # Test cases for migraine
    migraine_test_cases = [
        "I have a severe headache on one side of my head with nausea",
        "Migraine with aura and light sensitivity",
        "Throbbing headache with vomiting and dizziness",
        "One-sided headache with sound sensitivity",
        "Severe headache with visual disturbance",
        "Headache with photophobia and phonophobia"
    ]
    
    for i, symptoms in enumerate(migraine_test_cases, 1):
        print(f"\nTest {i}: '{symptoms}'")
        
        # Test validation
        validation = validate_symptoms_rule_based(symptoms, 'en')
        print(f"  Validation: {validation['is_valid']} (confidence: {validation['confidence']:.2f})")
        print(f"  Reason: {validation['reason']}")
        
        if not validation['is_valid']:
            print(f"  ❌ FAILED: Migraine symptoms rejected")
        else:
            print(f"  ✅ PASSED: Migraine symptoms accepted")

def test_uti_symptoms():
    """Test UTI symptom validation and prediction"""
    print("\n🧪 Testing UTI Symptoms...")
    
    # Test cases for UTI
    uti_test_cases = [
        "Burning sensation when urinating",
        "Frequent urination with strong-smelling urine",
        "Painful urination and lower abdominal pain",
        "Blood in urine and urinary urgency",
        "Cloudy urine with pelvic pain",
        "UTI symptoms with frequent urination"
    ]
    
    for i, symptoms in enumerate(uti_test_cases, 1):
        print(f"\nTest {i}: '{symptoms}'")
        
        # Test validation
        validation = validate_symptoms_rule_based(symptoms, 'en')
        print(f"  Validation: {validation['is_valid']} (confidence: {validation['confidence']:.2f})")
        print(f"  Reason: {validation['reason']}")
        
        if not validation['is_valid']:
            print(f"  ❌ FAILED: UTI symptoms rejected")
        else:
            print(f"  ✅ PASSED: UTI symptoms accepted")

def test_somali_symptoms():
    """Test Somali symptom validation"""
    print("\n🧪 Testing Somali Symptoms...")
    
    # Test cases for Somali
    somali_test_cases = [
        "Madax xanuun daran iyo indho xanuun",
        "Kaadi xanuun iyo calool hoose xanuun",
        "Qandho iyo dhidid habeenkii",
        "Sanka duufsan iyo qufac"
    ]
    
    for i, symptoms in enumerate(somali_test_cases, 1):
        print(f"\nTest {i}: '{symptoms}'")
        
        # Test validation
        validation = validate_symptoms_rule_based(symptoms, 'som')
        print(f"  Validation: {validation['is_valid']} (confidence: {validation['confidence']:.2f})")
        print(f"  Reason: {validation['reason']}")
        
        if not validation['is_valid']:
            print(f"  ❌ FAILED: Somali symptoms rejected")
        else:
            print(f"  ✅ PASSED: Somali symptoms accepted")

def test_edge_cases():
    """Test edge cases and mixed symptoms"""
    print("\n🧪 Testing Edge Cases...")
    
    edge_test_cases = [
        "I'm feeling sick with headache and nausea",  # General medical context
        "Having trouble with pain in my stomach",     # Medical context
        "Experiencing discomfort and fatigue",        # Medical context
        "Hello how are you",                          # Non-medical
        "What is the weather like",                   # Non-medical
        "Testing 123",                                # Non-medical
    ]
    
    for i, symptoms in enumerate(edge_test_cases, 1):
        print(f"\nTest {i}: '{symptoms}'")
        
        # Test validation
        validation = validate_symptoms_rule_based(symptoms, 'en')
        print(f"  Validation: {validation['is_valid']} (confidence: {validation['confidence']:.2f})")
        print(f"  Reason: {validation['reason']}")
        
        if symptoms.startswith(('Hello', 'What is', 'Testing')):
            expected = False
        else:
            expected = True
            
        if validation['is_valid'] == expected:
            print(f"  ✅ PASSED: Expected {expected}")
        else:
            print(f"  ❌ FAILED: Expected {expected}, got {validation['is_valid']}")

def main():
    """Run all tests"""
    print("🔧 Testing Disease Prediction Fixes")
    print("=" * 50)
    
    test_migraine_symptoms()
    test_uti_symptoms()
    test_somali_symptoms()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\nKey improvements made:")
    print("✅ Enhanced migraine symptom keywords")
    print("✅ Enhanced UTI symptom keywords")
    print("✅ More lenient symptom validation")
    print("✅ Better medical context detection")
    print("✅ Reduced confidence threshold")
    print("✅ Improved disease rules")

if __name__ == "__main__":
    main()

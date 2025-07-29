#!/usr/bin/env python3
"""
Test script for Somali disease rules integration
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_somali_disease_rules():
    """Test the Somali disease rules integration"""
    
    # Import the functions
    from app import apply_somali_disease_rules, DISEASE_RULES
    
    print("🧪 Testing Somali Disease Rules Integration")
    print("=" * 60)
    
    # Check if disease rules are available
    if not DISEASE_RULES:
        print("❌ Disease rules not available")
        print("   Make sure disease_rules.py is in the same directory")
        return False
    
    print("✅ Disease rules available")
    print(f"📊 Loaded {len(DISEASE_RULES)} disease rules:")
    for disease in DISEASE_RULES.keys():
        print(f"   - {disease}")
    
    # Test cases with Somali symptoms
    test_cases = [
        {
            "symptoms": "Waxaan qabaa qandho iyo madax xanuun",
            "expected_boost": ["malaria", "migraine"],
            "description": "Malaria symptoms (fever + headache)"
        },
        {
            "symptoms": "Waxaan qabaa madax xanuun daran iyo indho xanuun",
            "expected_boost": ["migraine"],
            "description": "Strong migraine symptoms"
        },
        {
            "symptoms": "Waxaan qabaa sanka duufsan iyo qufac",
            "expected_boost": ["common cold"],
            "description": "Common cold symptoms"
        },
        {
            "symptoms": "Waxaan qabaa xummad raagta iyo caloosha xanuunka",
            "expected_boost": ["typhoid"],
            "description": "Typhoid symptoms"
        },
        {
            "symptoms": "Waxaan qabaa qandho iyo sanka duufsan",
            "expected_boost": ["malaria", "common cold"],
            "description": "Mixed symptoms (malaria + cold)"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"   Symptoms: {test_case['symptoms']}")
        print(f"   Expected boost: {test_case['expected_boost']}")
        
        try:
            # Create mock ensemble predictions
            mock_predictions = {
                "malaria": 0.3,
                "migraine": 0.25,
                "typhoid": 0.2,
                "common cold": 0.25
            }
            
            # Apply Somali disease rules
            adjusted_predictions, adjusted_confidences = apply_somali_disease_rules(
                test_case['symptoms'],
                mock_predictions,
                mock_predictions
            )
            
            print(f"   ✅ Rules applied successfully")
            print(f"   📊 Adjusted predictions:")
            
            for disease, confidence in adjusted_confidences.items():
                original = mock_predictions.get(disease, 0)
                change = confidence - original
                change_symbol = "+" if change > 0 else ""
                print(f"      {disease}: {original:.3f} -> {confidence:.3f} ({change_symbol}{change:.3f})")
            
            # Check if expected diseases were boosted
            boosted_diseases = []
            for disease, confidence in adjusted_confidences.items():
                original = mock_predictions.get(disease, 0)
                if confidence > original:
                    boosted_diseases.append(disease)
            
            print(f"   🎯 Boosted diseases: {boosted_diseases}")
            
            # Check if results match expectations
            expected_matches = sum(1 for disease in test_case['expected_boost'] if disease in boosted_diseases)
            total_expected = len(test_case['expected_boost'])
            
            if expected_matches == total_expected:
                print(f"   ✅ PASS: All expected diseases were boosted")
                passed = True
            else:
                print(f"   ❌ FAIL: Only {expected_matches}/{total_expected} expected diseases were boosted")
                passed = False
            
            results.append({
                'test_case': i,
                'symptoms': test_case['symptoms'],
                'expected_boost': test_case['expected_boost'],
                'actual_boost': boosted_diseases,
                'passed': passed
            })
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({
                'test_case': i,
                'symptoms': test_case['symptoms'],
                'error': str(e),
                'passed': False
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.get('passed', False))
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️ Some tests failed")
        return False

def test_disease_rules_structure():
    """Test the structure of disease rules"""
    
    from app import DISEASE_RULES
    
    print("\n🔍 Testing Disease Rules Structure")
    print("=" * 40)
    
    if not DISEASE_RULES:
        print("❌ No disease rules found")
        return False
    
    for disease, rules in DISEASE_RULES.items():
        print(f"\n📋 Disease: {disease}")
        
        boost_keywords = rules.get('boost_keywords', [])
        penalize_keywords = rules.get('penalize_keywords', [])
        
        print(f"   ✅ Boost keywords ({len(boost_keywords)}): {boost_keywords}")
        print(f"   ❌ Penalize keywords ({len(penalize_keywords)}): {penalize_keywords}")
        
        if not boost_keywords and not penalize_keywords:
            print(f"   ⚠️ Warning: No keywords defined for {disease}")
    
    return True

if __name__ == "__main__":
    print("🧪 Somali Disease Rules Integration Test")
    print("=" * 60)
    
    # Test structure first
    structure_ok = test_disease_rules_structure()
    
    if structure_ok:
        # Test functionality
        success = test_somali_disease_rules()
        sys.exit(0 if success else 1)
    else:
        print("❌ Disease rules structure test failed")
        sys.exit(1)
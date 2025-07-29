#!/usr/bin/env python3
"""
Comprehensive test script for Somali disease rules integration
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_complete_somali_rules():
    """Test the complete Somali disease rules integration"""
    
    # Import the functions
    from app import (
        pre_filter_diseases_by_somali_symptoms, 
        apply_somali_disease_rules, 
        DISEASE_RULES
    )
    
    print("🧪 Testing Complete Somali Disease Rules Integration")
    print("=" * 70)
    
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
            "expected_pre_filter": ["malaria", "migraine"],
            "expected_boost": ["malaria", "migraine"],
            "description": "Malaria symptoms (fever + headache)"
        },
        {
            "symptoms": "Waxaan qabaa madax xanuun daran iyo indho xanuun",
            "expected_pre_filter": ["migraine"],
            "expected_boost": ["migraine"],
            "description": "Strong migraine symptoms"
        },
        {
            "symptoms": "Waxaan qabaa sanka duufsan iyo qufac",
            "expected_pre_filter": ["common cold"],
            "expected_boost": ["common cold"],
            "description": "Common cold symptoms"
        },
        {
            "symptoms": "Waxaan qabaa xummad raagta iyo caloosha xanuunka",
            "expected_pre_filter": ["typhoid"],
            "expected_boost": ["typhoid"],
            "description": "Typhoid symptoms"
        },
        {
            "symptoms": "Waxaan qabaa qandho iyo qufac iyo neefsasho gaaban",
            "expected_pre_filter": ["malaria", "pneumonia"],
            "expected_boost": ["malaria", "pneumonia"],
            "description": "Pneumonia symptoms (fever + cough + shortness of breath)"
        },
        {
            "symptoms": "Waxaan qabaa qandho iyo sanka duufsan",
            "expected_pre_filter": ["malaria", "common cold"],
            "expected_boost": ["malaria", "common cold"],
            "description": "Mixed symptoms (malaria + cold)"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['description']}")
        print(f"   Symptoms: {test_case['symptoms']}")
        print(f"   Expected pre-filter: {test_case['expected_pre_filter']}")
        print(f"   Expected boost: {test_case['expected_boost']}")
        
        try:
            # Test 1: Pre-filtering
            print(f"\n   📋 Testing Pre-filtering:")
            pre_filtered = pre_filter_diseases_by_somali_symptoms(test_case['symptoms'])
            
            if pre_filtered:
                print(f"      ✅ Pre-filtered diseases: {pre_filtered}")
                
                # Check if pre-filtering matches expectations
                expected_matches = sum(1 for disease in test_case['expected_pre_filter'] if disease in pre_filtered)
                total_expected = len(test_case['expected_pre_filter'])
                
                if expected_matches == total_expected:
                    print(f"      ✅ PASS: All expected diseases in pre-filter")
                    pre_filter_passed = True
                else:
                    print(f"      ❌ FAIL: Only {expected_matches}/{total_expected} expected diseases in pre-filter")
                    pre_filter_passed = False
            else:
                print(f"      ⚠️ No diseases pre-filtered")
                pre_filter_passed = False
            
            # Test 2: Rule application
            print(f"\n   🎯 Testing Rule Application:")
            
            # Create mock ensemble predictions
            mock_predictions = {
                "malaria": 0.3,
                "migraine": 0.25,
                "typhoid": 0.2,
                "common cold": 0.25,
                "pneumonia": 0.2
            }
            
            # Apply Somali disease rules
            adjusted_predictions, adjusted_confidences = apply_somali_disease_rules(
                test_case['symptoms'],
                mock_predictions,
                mock_predictions
            )
            
            print(f"      ✅ Rules applied successfully")
            print(f"      📊 Adjusted predictions:")
            
            boosted_diseases = []
            for disease, confidence in adjusted_confidences.items():
                original = mock_predictions.get(disease, 0)
                change = confidence - original
                change_symbol = "+" if change > 0 else ""
                print(f"         {disease}: {original:.3f} -> {confidence:.3f} ({change_symbol}{change:.3f})")
                
                if confidence > original:
                    boosted_diseases.append(disease)
            
            print(f"      🎯 Boosted diseases: {boosted_diseases}")
            
            # Check if rule application matches expectations
            expected_matches = sum(1 for disease in test_case['expected_boost'] if disease in boosted_diseases)
            total_expected = len(test_case['expected_boost'])
            
            if expected_matches == total_expected:
                print(f"      ✅ PASS: All expected diseases were boosted")
                rule_application_passed = True
            else:
                print(f"      ❌ FAIL: Only {expected_matches}/{total_expected} expected diseases were boosted")
                rule_application_passed = False
            
            # Overall test result
            overall_passed = pre_filter_passed and rule_application_passed
            
            results.append({
                'test_case': i,
                'symptoms': test_case['symptoms'],
                'expected_pre_filter': test_case['expected_pre_filter'],
                'expected_boost': test_case['expected_boost'],
                'actual_pre_filter': pre_filtered,
                'actual_boost': boosted_diseases,
                'pre_filter_passed': pre_filter_passed,
                'rule_application_passed': rule_application_passed,
                'overall_passed': overall_passed
            })
            
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({
                'test_case': i,
                'symptoms': test_case['symptoms'],
                'error': str(e),
                'overall_passed': False
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r.get('overall_passed', False))
    total = len(results)
    
    print(f"✅ Overall Passed: {passed}/{total}")
    print(f"❌ Overall Failed: {total - passed}/{total}")
    
    # Detailed breakdown
    pre_filter_passed = sum(1 for r in results if r.get('pre_filter_passed', False))
    rule_app_passed = sum(1 for r in results if r.get('rule_application_passed', False))
    
    print(f"\n📋 Detailed Results:")
    print(f"   Pre-filtering: {pre_filter_passed}/{total} passed")
    print(f"   Rule application: {rule_app_passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Somali disease rules integration is working correctly.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the detailed results above.")
        return False

def test_disease_rules_coverage():
    """Test coverage of disease rules"""
    
    from app import DISEASE_RULES
    
    print("\n🔍 Testing Disease Rules Coverage")
    print("=" * 50)
    
    if not DISEASE_RULES:
        print("❌ No disease rules found")
        return False
    
    total_keywords = 0
    diseases_with_rules = 0
    
    for disease, rules in DISEASE_RULES.items():
        boost_keywords = rules.get('boost_keywords', [])
        penalize_keywords = rules.get('penalize_keywords', [])
        
        total_keywords += len(boost_keywords) + len(penalize_keywords)
        
        if boost_keywords or penalize_keywords:
            diseases_with_rules += 1
            print(f"✅ {disease}: {len(boost_keywords)} boost, {len(penalize_keywords)} penalize keywords")
        else:
            print(f"⚠️ {disease}: No keywords defined")
    
    print(f"\n📊 Coverage Summary:")
    print(f"   Diseases with rules: {diseases_with_rules}/{len(DISEASE_RULES)}")
    print(f"   Total keywords: {total_keywords}")
    print(f"   Average keywords per disease: {total_keywords/len(DISEASE_RULES):.1f}")
    
    return diseases_with_rules == len(DISEASE_RULES)

if __name__ == "__main__":
    print("🧪 Complete Somali Disease Rules Integration Test")
    print("=" * 70)
    
    # Test coverage first
    coverage_ok = test_disease_rules_coverage()
    
    if coverage_ok:
        # Test functionality
        success = test_complete_somali_rules()
        sys.exit(0 if success else 1)
    else:
        print("❌ Disease rules coverage test failed")
        sys.exit(1)
#!/usr/bin/env python3
"""
Test script for OpenAI symptom validation
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_openai_validation():
    """Test the OpenAI symptom validation function"""
    
    # Import the validation function
    from app import validate_symptoms_with_openai, openai_client
    
    print("🧪 Testing OpenAI Symptom Validation")
    print("=" * 50)
    
    # Check if OpenAI is available
    if not openai_client:
        print("❌ OpenAI client not available")
        print("   Make sure OPENAI_API_KEY is set in your .env file")
        return False
    
    print("✅ OpenAI client available")
    
    # Test cases
    test_cases = [
        {
            "symptoms": "I have a severe headache and high fever",
            "language": "en",
            "expected": True
        },
        {
            "symptoms": "Waxaan qabaa madax xanuun iyo qandho",
            "language": "som",
            "expected": True
        },
        {
            "symptoms": "Hello world, how are you today?",
            "language": "en",
            "expected": False
        },
        {
            "symptoms": "I love pizza and movies",
            "language": "en",
            "expected": False
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['symptoms']}")
        print(f"   Language: {test_case['language']}")
        print(f"   Expected valid: {test_case['expected']}")
        
        try:
            result = validate_symptoms_with_openai(
                test_case['symptoms'], 
                test_case['language']
            )
            
            is_valid = result['is_valid']
            confidence = result['confidence']
            reason = result['reason']
            
            print(f"   ✅ Result: {is_valid} (confidence: {confidence:.2f})")
            print(f"   📝 Reason: {reason}")
            
            if result['suggestions']:
                print(f"   💡 Suggestions: {', '.join(result['suggestions'][:2])}")
            
            # Check if result matches expectation
            if is_valid == test_case['expected']:
                print(f"   ✅ PASS: Result matches expectation")
            else:
                print(f"   ❌ FAIL: Result doesn't match expectation")
            
            results.append({
                'test_case': i,
                'symptoms': test_case['symptoms'],
                'expected': test_case['expected'],
                'actual': is_valid,
                'confidence': confidence,
                'reason': reason,
                'passed': is_valid == test_case['expected']
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
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
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

if __name__ == "__main__":
    success = test_openai_validation()
    sys.exit(0 if success else 1)
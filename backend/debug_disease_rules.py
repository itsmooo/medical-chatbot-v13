#!/usr/bin/env python3
"""
Debug script to test disease rules with specific symptoms
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def debug_disease_rules():
    """Debug the disease rules with specific symptoms"""
    
    # Import the functions
    from app import apply_somali_disease_rules, DISEASE_RULES
    
    print("🔍 DEBUGGING DISEASE RULES")
    print("=" * 50)
    
    # Test with the specific symptoms you mentioned
    test_symptoms = "dhidid, qandho, shuban"
    
    print(f"🔍 Testing symptoms: '{test_symptoms}'")
    print(f"🔍 Disease rules available: {bool(DISEASE_RULES)}")
    print(f"🔍 Number of disease rules: {len(DISEASE_RULES) if DISEASE_RULES else 0}")
    
    if DISEASE_RULES:
        print(f"🔍 Available diseases: {list(DISEASE_RULES.keys())}")
    
    # Create mock ensemble predictions
    mock_predictions = {
        "malaria": 0.3,
        "migraine": 0.25,
        "typhoid": 0.2,
        "common cold": 0.25,
        "pneumonia": 0.2
    }
    
    print(f"\n🔍 Mock ensemble predictions: {mock_predictions}")
    
    # Apply Somali disease rules
    print(f"\n🔍 Applying Somali disease rules...")
    adjusted_predictions, adjusted_confidences = apply_somali_disease_rules(
        test_symptoms,
        mock_predictions,
        mock_predictions
    )
    
    print(f"\n🔍 RESULTS:")
    print(f"🔍 Adjusted predictions: {adjusted_predictions}")
    print(f"🔍 Adjusted confidences: {adjusted_confidences}")
    
    # Show the changes
    print(f"\n🔍 CHANGES:")
    for disease, confidence in adjusted_confidences.items():
        original = mock_predictions.get(disease, 0)
        change = confidence - original
        change_symbol = "+" if change > 0 else ""
        print(f"   {disease}: {original:.3f} -> {confidence:.3f} ({change_symbol}{change:.3f})")
    
    # Find the best prediction
    if adjusted_confidences:
        best_disease = max(adjusted_confidences, key=adjusted_confidences.get)
        best_confidence = adjusted_confidences[best_disease]
        original_best = max(mock_predictions, key=mock_predictions.get)
        original_confidence = mock_predictions[original_best]
        
        print(f"\n🔍 FINAL RESULT:")
        print(f"🔍 Original best: '{original_best}' ({original_confidence:.3f})")
        print(f"🔍 New best: '{best_disease}' ({best_confidence:.3f})")
        
        if best_disease != original_best:
            print(f"✅ PREDICTION CHANGED: '{original_best}' -> '{best_disease}'")
        else:
            print(f"✅ PREDICTION CONFIRMED: '{best_disease}'")
    
    # Manual analysis
    print(f"\n🔍 MANUAL ANALYSIS:")
    symptoms_lower = test_symptoms.lower()
    print(f"🔍 Symptoms (lowercase): '{symptoms_lower}'")
    
    for disease, rules in DISEASE_RULES.items():
        print(f"\n🔍 Analyzing '{disease}':")
        
        boost_matches = []
        penalize_matches = []
        
        # Check boost keywords
        for keyword in rules.get('boost_keywords', []):
            if keyword.lower() in symptoms_lower:
                boost_matches.append(keyword)
                print(f"   ✅ BOOST: '{keyword}' found")
            else:
                print(f"   ❌ BOOST: '{keyword}' not found")
        
        # Check penalize keywords
        for keyword in rules.get('penalize_keywords', []):
            if keyword.lower() in symptoms_lower:
                penalize_matches.append(keyword)
                print(f"   ❌ PENALIZE: '{keyword}' found")
            else:
                print(f"   ✅ PENALIZE: '{keyword}' not found")
        
        net_score = len(boost_matches) - len(penalize_matches)
        print(f"   📊 Net score: {net_score} (boost: {len(boost_matches)}, penalize: {len(penalize_matches)})")

if __name__ == "__main__":
    debug_disease_rules()
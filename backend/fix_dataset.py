#!/usr/bin/env python3
"""
Dataset Fix Script for Medical Disease Prediction
Fixes incorrect symptoms and improves data quality
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

def fix_migraine_symptoms(symptoms_text):
    """Fix migraine symptoms to be more accurate and specific"""
    
    # Remove incorrect symptoms that don't belong to migraine
    incorrect_symptoms = [
        'increased urination', 'fluid retention', 'constipation',
        'frequent yawning', 'neck stiffness'
    ]
    
    # Split symptoms and clean them
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Skip incorrect symptoms
        if any(incorrect in symptom_lower for incorrect in incorrect_symptoms):
            continue
            
        # Keep valid migraine symptoms
        if any(valid in symptom_lower for valid in [
            'headache', 'migraine', 'pain', 'nausea', 'vomiting',
            'light sensitivity', 'sound sensitivity', 'aura',
            'visual disturbance', 'throbbing', 'pulsing'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add some default migraine symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Severe headache, often on one side of the head',
            'Nausea and vomiting',
            'Sensitivity to light and sound',
            'Throbbing or pulsing pain'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_uti_symptoms(symptoms_text):
    """Fix UTI symptoms to be more complete and accurate"""
    
    # Complete the cut-off symptoms
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Complete cut-off symptoms
        if 'strong-smelling urine' in symptom_lower:
            cleaned_symptoms.append('Strong-smelling urine')
        elif 'urine that looks cloudy' in symptom_lower:
            cleaned_symptoms.append('Urine that looks cloudy or murky')
        elif 'urine that appears red' in symptom_lower or 'blood in the urine' in symptom_lower:
            cleaned_symptoms.append('Blood in urine (red, pink, or cola-colored urine)')
        elif 'strong urge to urinate' in symptom_lower:
            cleaned_symptoms.append('Strong urge to urinate that doesn\'t go away')
        elif 'urinating often' in symptom_lower:
            cleaned_symptoms.append('Frequent urination, often in small amounts')
        elif 'burning feeling when urinating' in symptom_lower:
            cleaned_symptoms.append('Burning sensation when urinating')
        elif 'pelvic pain' in symptom_lower:
            cleaned_symptoms.append('Pelvic pain, especially in women')
        elif 'lower abdominal pain' in symptom_lower:
            cleaned_symptoms.append('Lower abdominal pain or discomfort')
        else:
            # Keep other valid symptoms
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default UTI symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Frequent urination',
            'Burning sensation when urinating',
            'Strong urge to urinate',
            'Cloudy or strong-smelling urine',
            'Lower abdominal pain'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_diabetes_symptoms(symptoms_text):
    """Fix diabetes symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid diabetes symptoms
        if any(valid in symptom_lower for valid in [
            'thirst', 'thirsty', 'urination', 'urinate', 'hungry', 'hunger',
            'weight loss', 'fatigue', 'tired', 'weakness', 'blurred vision',
            'blurry', 'vision', 'diabetes', 'sugar', 'blood sugar'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default diabetes symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Excessive thirst',
            'Frequent urination',
            'Increased hunger',
            'Unexplained weight loss',
            'Fatigue and weakness',
            'Blurred vision'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_malaria_symptoms(symptoms_text):
    """Fix malaria symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid malaria symptoms
        if any(valid in symptom_lower for valid in [
            'fever', 'chills', 'sweating', 'headache', 'muscle pain',
            'fatigue', 'nausea', 'vomiting', 'malaria', 'mosquito',
            'travel', 'safari', 'tropical'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default malaria symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'High fever with chills',
            'Sweating and shaking',
            'Severe headache',
            'Muscle and joint pain',
            'Fatigue and weakness',
            'Nausea and vomiting'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_pneumonia_symptoms(symptoms_text):
    """Fix pneumonia symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid pneumonia symptoms
        if any(valid in symptom_lower for valid in [
            'cough', 'fever', 'difficulty breathing', 'shortness of breath',
            'chest pain', 'fatigue', 'sweating', 'chills', 'pneumonia',
            'lung', 'respiratory', 'breathing'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default pneumonia symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Persistent cough with phlegm',
            'High fever',
            'Difficulty breathing',
            'Chest pain when breathing',
            'Fatigue and weakness',
            'Sweating and chills'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_typhoid_symptoms(symptoms_text):
    """Fix typhoid symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid typhoid symptoms
        if any(valid in symptom_lower for valid in [
            'fever', 'headache', 'stomach pain', 'abdominal pain',
            'weakness', 'fatigue', 'typhoid', 'rose spots', 'constipation',
            'diarrhea', 'loss of appetite'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default typhoid symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Prolonged high fever',
            'Severe headache',
            'Stomach pain and discomfort',
            'Weakness and fatigue',
            'Loss of appetite',
            'Rose-colored spots on chest'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_common_cold_symptoms(symptoms_text):
    """Fix common cold symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid cold symptoms
        if any(valid in symptom_lower for valid in [
            'runny nose', 'stuffy nose', 'congestion', 'cough',
            'sore throat', 'sneezing', 'cold', 'mild fever',
            'fatigue', 'headache'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default cold symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Runny or stuffy nose',
            'Sneezing',
            'Sore throat',
            'Mild cough',
            'Mild fever',
            'Fatigue'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_fungal_infection_symptoms(symptoms_text):
    """Fix fungal infection symptoms to be more accurate"""
    
    symptoms_list = [s.strip() for s in symptoms_text.split(';') if s.strip()]
    cleaned_symptoms = []
    
    for symptom in symptoms_list:
        symptom_lower = symptom.lower()
        
        # Keep valid fungal infection symptoms
        if any(valid in symptom_lower for valid in [
            'itchy', 'itching', 'rash', 'skin', 'redness',
            'fungal', 'infection', 'peeling', 'white patches',
            'ringworm', 'athlete foot'
        ]):
            cleaned_symptoms.append(symptom)
    
    # If no valid symptoms remain, add default fungal infection symptoms
    if not cleaned_symptoms:
        cleaned_symptoms = [
            'Itchy skin rash',
            'Redness and inflammation',
            'Skin peeling or flaking',
            'White or colored patches',
            'Burning sensation',
            'Cracked or dry skin'
        ]
    
    return '; '.join(cleaned_symptoms)

def fix_dataset():
    """Main function to fix the entire dataset"""
    
    print("🔧 Starting dataset fix process...")
    
    # Load the dataset
    input_file = 'data/medical_chatbot_dataset-R -.csv'
    output_file = 'data/medical_chatbot_dataset_fixed.csv'
    
    try:
        df = pd.read_csv(input_file)
        print(f"✅ Loaded dataset with {len(df)} rows")
        print(f"📊 Original disease distribution:")
        print(df['Disease'].value_counts())
        
        # Create a copy for fixing
        df_fixed = df.copy()
        
        # Fix symptoms for each disease
        disease_fixers = {
            'Migraine': fix_migraine_symptoms,
            'Urinary Tract Infection': fix_uti_symptoms,
            'Diabetes': fix_diabetes_symptoms,
            'Malaria': fix_malaria_symptoms,
            'Pneumonia': fix_pneumonia_symptoms,
            'Typhoid': fix_typhoid_symptoms,
            'Common Cold': fix_common_cold_symptoms,
            'Fungal Infections': fix_fungal_infection_symptoms
        }
        
        fixed_count = 0
        for disease, fixer_func in disease_fixers.items():
            print(f"\n🔧 Fixing {disease} symptoms...")
            
            # Get rows for this disease
            disease_mask = df_fixed['Disease'] == disease
            disease_rows = df_fixed[disease_mask]
            
            # Apply the fixer function
            for idx in disease_rows.index:
                original_symptoms = df_fixed.loc[idx, 'Symptoms']
                fixed_symptoms = fixer_func(original_symptoms)
                
                if fixed_symptoms != original_symptoms:
                    df_fixed.loc[idx, 'Symptoms'] = fixed_symptoms
                    fixed_count += 1
                    print(f"   Fixed row {idx}: {original_symptoms[:50]}... -> {fixed_symptoms[:50]}...")
        
        print(f"\n✅ Fixed {fixed_count} symptom entries")
        
        # Save the fixed dataset
        df_fixed.to_csv(output_file, index=False)
        print(f"💾 Saved fixed dataset to {output_file}")
        
        # Show sample of fixed symptoms
        print(f"\n📋 Sample of fixed symptoms:")
        for disease in disease_fixers.keys():
            sample = df_fixed[df_fixed['Disease'] == disease]['Symptoms'].iloc[0]
            print(f"\n{disease}:")
            print(f"  {sample[:100]}...")
        
        return df_fixed
        
    except Exception as e:
        print(f"❌ Error fixing dataset: {e}")
        return None

if __name__ == "__main__":
    fixed_df = fix_dataset()
    if fixed_df is not None:
        print("\n🎉 Dataset fix completed successfully!")
        print("You can now retrain your models with the improved dataset.")
    else:
        print("\n❌ Dataset fix failed!")

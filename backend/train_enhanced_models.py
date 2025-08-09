#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_recall_fscore_support
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import pickle
import warnings
from collections import Counter
import json
import requests
import re
from io import StringIO

warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")
SHOW_PLOTS = os.getenv('SHOW_PLOTS', '0') == '1'

# ====================== 1. Enhanced Data Loading & Preprocessing ======================

def create_directories():
    """Create necessary directories for outputs"""
    directories = ['disease_figures', 'disease_models', 'disease_reports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Created directories")

def load_real_dataset():
    """Load the medical chatbot dataset from a local CSV file or create synthetic data"""
    print("📥 Attempting to load medical dataset...")
    
    # Try backend/data first, then CWD
    candidate_paths = [
        os.path.join('data', 'medical_chatbot_dataset-R -.csv'),
        'medical_chatbot_dataset-R -.csv'
    ]
    
    for local_file_path in candidate_paths:
        if os.path.exists(local_file_path):
            try:
                df = pd.read_csv(local_file_path)
                print(f"✅ Dataset loaded successfully from: {local_file_path}!")
                print(f"Dataset shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                return df
            except Exception as e:
                print(f"❌ Error reading local file {local_file_path}: {e}")
    
    print("Local file not found or invalid, creating fallback synthetic dataset...")
    return create_fallback_dataset()

def create_fallback_dataset():
    """Create fallback dataset if URL fails"""
    print("Creating fallback synthetic dataset...")
    
    diseases = [
        'Malaria', 'Typhoid', 'Migraine', 'Pneumonia', 'Fungal Infection',
        'Urinary Tract Infection', 'Diabetes', 'Common Cold', 'Hypertension', 'Gastritis'
    ]
    
    symptoms_list = [
        'Fever', 'Chills', 'Headache', 'Fatigue', 'Abdominal Pain', 
        'Burning Sensation', 'Frequent Urination', 'Cough', 'Nausea',
        'Vomiting', 'Muscle Pain', 'Joint Pain', 'Skin Rash', 'Dizziness',
        'Chest Pain', 'Shortness of Breath', 'Night Sweats', 'Weight Loss',
        'Blurred Vision', 'Excessive Thirst', 'Loss of Appetite', 'Constipation'
    ]
    
    # Disease-symptom associations
    disease_symptoms = {
        'Malaria': {
            'primary': ['Fever', 'Chills', 'Headache', 'Fatigue', 'Muscle Pain', 'Night Sweats'],
            'secondary': ['Nausea', 'Vomiting', 'Dizziness', 'Joint Pain'],
            'probability': 0.8
        },
        'Typhoid': {
            'primary': ['Fever', 'Headache', 'Abdominal Pain', 'Fatigue', 'Loss of Appetite'],
            'secondary': ['Nausea', 'Vomiting', 'Constipation', 'Muscle Pain'],
            'probability': 0.85
        },
        'Migraine': {
            'primary': ['Headache', 'Nausea', 'Dizziness'],
            'secondary': ['Fatigue', 'Blurred Vision', 'Vomiting'],
            'probability': 0.9
        },
        'Pneumonia': {
            'primary': ['Fever', 'Cough', 'Chest Pain', 'Shortness of Breath', 'Fatigue'],
            'secondary': ['Headache', 'Muscle Pain', 'Chills'],
            'probability': 0.85
        },
        'Fungal Infection': {
            'primary': ['Skin Rash', 'Fatigue'],
            'secondary': ['Fever', 'Joint Pain'],
            'probability': 0.7
        },
        'Urinary Tract Infection': {
            'primary': ['Burning Sensation', 'Frequent Urination', 'Fever'],
            'secondary': ['Abdominal Pain', 'Fatigue', 'Nausea'],
            'probability': 0.8
        },
        'Diabetes': {
            'primary': ['Frequent Urination', 'Excessive Thirst', 'Fatigue', 'Blurred Vision'],
            'secondary': ['Weight Loss', 'Dizziness', 'Headache'],
            'probability': 0.75
        },
        'Common Cold': {
            'primary': ['Cough', 'Headache', 'Fatigue'],
            'secondary': ['Fever', 'Muscle Pain', 'Nausea'],
            'probability': 0.6
        },
        'Hypertension': {
            'primary': ['Headache', 'Dizziness', 'Chest Pain'],
            'secondary': ['Fatigue', 'Blurred Vision', 'Shortness of Breath'],
            'probability': 0.7
        },
        'Gastritis': {
            'primary': ['Abdominal Pain', 'Nausea', 'Loss of Appetite'],
            'secondary': ['Vomiting', 'Fatigue', 'Headache'],
            'probability': 0.8
        }
    }
    
    # Generate synthetic data
    np.random.seed(42)
    data = []
    
    for _ in range(2000):
        disease = np.random.choice(diseases)
        disease_info = disease_symptoms[disease]
        
        selected_symptoms = []
        
        # Primary symptoms
        for symptom in disease_info['primary']:
            if np.random.random() < disease_info['probability']:
                selected_symptoms.append(symptom)
        
        # Secondary symptoms
        for symptom in disease_info['secondary']:
            if np.random.random() < (disease_info['probability'] * 0.6):
                selected_symptoms.append(symptom)
        
        # Add noise
        noise_symptoms = np.random.choice(symptoms_list, size=np.random.randint(0, 2))
        for symptom in noise_symptoms:
            if np.random.random() < 0.1:
                selected_symptoms.append(symptom)
        
        if not selected_symptoms:
            selected_symptoms = [np.random.choice(disease_info['primary'])]
        
        symptoms_str = '; '.join(set(selected_symptoms))
        data.append({'Disease': disease, 'Symptoms': symptoms_str})
    
    df = pd.DataFrame(data)
    return df

def clean_and_preprocess_data(df):
    """Clean and preprocess the loaded dataset"""
    print("🧹 Cleaning and preprocessing data...")
    
    # Make a copy
    data = df.copy()
    
    # Basic info about the dataset
    print(f"Original dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    print(f"Missing values:\n{data.isnull().sum()}")
    
    # Handle missing values
    if data.isnull().sum().sum() > 0:
        print("Handling missing values...")
        # Drop rows with missing Disease or Symptoms
        data = data.dropna(subset=['Disease', 'Symptoms'])
        print(f"Shape after removing missing values: {data.shape}")
    
    # Clean text data
    print("Cleaning text data...")
    
    # Clean Disease names
    data['Disease'] = data['Disease'].str.strip()
    data['Disease'] = data['Disease'].str.title()
    # Normalize plural/synonyms
    data['Disease'] = data['Disease'].replace({
        'Fungal Infections': 'Fungal Infection'
    })
    
    # Clean Symptoms
    data['Symptoms'] = data['Symptoms'].str.strip()
    
    # Remove any rows with empty symptoms or diseases
    data = data[(data['Disease'].str.len() > 0) & (data['Symptoms'].str.len() > 0)]
    
    # Check for duplicate rows
    duplicates = data.duplicated().sum()
    if duplicates > 0:
        print(f"Removing {duplicates} duplicate rows...")
        data = data.drop_duplicates()
    
    # Display disease distribution
    print(f"\nDisease distribution:")
    disease_counts = data['Disease'].value_counts()
    print(disease_counts)
    
    # Remove diseases with very few samples (less than 10)
    min_samples = 10
    diseases_to_keep = disease_counts[disease_counts >= min_samples].index
    data = data[data['Disease'].isin(diseases_to_keep)]
    
    print(f"\nFinal dataset shape: {data.shape}")
    print(f"Number of diseases: {data['Disease'].nunique()}")
    print(f"Diseases included: {sorted(data['Disease'].unique())}")
    
    return data

def extract_symptoms_from_text(symptoms_text):
    """Extract individual symptoms from symptom text"""
    # Common separators in symptom descriptions
    separators = [';', ',', '—', '-', '•', '\n', '.', '|']
    
    # Replace separators with semicolon
    cleaned_text = symptoms_text
    for sep in separators:
        cleaned_text = cleaned_text.replace(sep, ';')
    
    # Split by semicolon and clean
    symptoms = []
    for symptom in cleaned_text.split(';'):
        symptom = symptom.strip()
        if symptom and len(symptom) > 2:  # Filter out very short strings
            # Remove common prefixes and suffixes
            symptom = re.sub(r'^(signs of|symptoms of|including|such as|like)\s*', '', symptom, flags=re.IGNORECASE)
            symptom = re.sub(r'\s*(in women|in men|especially|particularly).*$','', symptom, flags=re.IGNORECASE)
            symptom = symptom.strip()
            if symptom:
                symptoms.append(symptom)
    
    return symptoms

def standardize_symptoms(data):
    """Standardize symptom names across the dataset"""
    print("🔧 Standardizing symptom names...")
    
    # Extract all unique symptoms
    all_symptoms = set()
    for symptoms_text in data['Symptoms']:
        symptoms = extract_symptoms_from_text(symptoms_text)
        all_symptoms.update(symptoms)
    
    print(f"Found {len(all_symptoms)} unique symptom descriptions")
    
    # Create symptom mapping for standardization
    symptom_mapping = {}
    
    # Common symptom standardizations
    fever_terms = ['fever', 'high temperature', 'pyrexia', 'elevated temperature', 'hot', 'feverish']
    headache_terms = ['headache', 'head pain', 'cephalgia', 'migraine', 'head ache']
    nausea_terms = ['nausea', 'feeling sick', 'queasiness', 'sick feeling']
    fatigue_terms = ['fatigue', 'tiredness', 'weakness', 'exhaustion', 'tired', 'weak']
    cough_terms = ['cough', 'coughing', 'persistent cough', 'dry cough', 'wet cough']
    pain_terms = ['pain', 'ache', 'aching', 'discomfort', 'soreness']
    
    # Build mapping
    for symptom in all_symptoms:
        symptom_lower = symptom.lower()
        
        if any(term in symptom_lower for term in fever_terms):
            symptom_mapping[symptom] = 'Fever'
        elif any(term in symptom_lower for term in headache_terms):
            symptom_mapping[symptom] = 'Headache'
        elif any(term in symptom_lower for term in nausea_terms):
            symptom_mapping[symptom] = 'Nausea'
        elif any(term in symptom_lower for term in fatigue_terms):
            symptom_mapping[symptom] = 'Fatigue'
        elif any(term in symptom_lower for term in cough_terms):
            symptom_mapping[symptom] = 'Cough'
        elif 'abdominal' in symptom_lower and any(term in symptom_lower for term in pain_terms):
            symptom_mapping[symptom] = 'Abdominal Pain'
        elif 'chest' in symptom_lower and any(term in symptom_lower for term in pain_terms):
            symptom_mapping[symptom] = 'Chest Pain'
        elif 'muscle' in symptom_lower and any(term in symptom_lower for term in pain_terms):
            symptom_mapping[symptom] = 'Muscle Pain'
        elif 'joint' in symptom_lower and any(term in symptom_lower for term in pain_terms):
            symptom_mapping[symptom] = 'Joint Pain'
        elif 'burning' in symptom_lower:
            symptom_mapping[symptom] = 'Burning Sensation'
        elif 'frequent' in symptom_lower and 'urin' in symptom_lower:
            symptom_mapping[symptom] = 'Frequent Urination'
        elif 'vomit' in symptom_lower:
            symptom_mapping[symptom] = 'Vomiting'
        elif 'dizz' in symptom_lower:
            symptom_mapping[symptom] = 'Dizziness'
        elif 'rash' in symptom_lower or 'skin' in symptom_lower:
            symptom_mapping[symptom] = 'Skin Rash'
        elif 'chill' in symptom_lower:
            symptom_mapping[symptom] = 'Chills'
        elif 'sweat' in symptom_lower:
            symptom_mapping[symptom] = 'Night Sweats'
        elif 'thirst' in symptom_lower:
            symptom_mapping[symptom] = 'Excessive Thirst'
        elif 'weight' in symptom_lower and 'loss' in symptom_lower:
            symptom_mapping[symptom] = 'Weight Loss'
        elif 'appetite' in symptom_lower:
            symptom_mapping[symptom] = 'Loss of Appetite'
        elif 'breath' in symptom_lower and ('short' in symptom_lower or 'difficult' in symptom_lower):
            symptom_mapping[symptom] = 'Shortness of Breath'
        elif 'vision' in symptom_lower and 'blur' in symptom_lower:
            symptom_mapping[symptom] = 'Blurred Vision'
        elif 'constipat' in symptom_lower:
            symptom_mapping[symptom] = 'Constipation'
        else:
            # Keep original symptom name but clean it
            clean_symptom = symptom.title().strip()
            symptom_mapping[symptom] = clean_symptom
    
    # Apply standardization
    def standardize_symptom_text(symptoms_text):
        symptoms = extract_symptoms_from_text(symptoms_text)
        standardized_symptoms = []
        for symptom in symptoms:
            if symptom in symptom_mapping:
                standardized_symptoms.append(symptom_mapping[symptom])
            else:
                standardized_symptoms.append(symptom.title().strip())
        return '; '.join(list(set(standardized_symptoms)))  # Remove duplicates
    
    data['Symptoms'] = data['Symptoms'].apply(standardize_symptom_text)
    
    # Get final symptom list
    final_symptoms = set()
    for symptoms_text in data['Symptoms']:
        symptoms = symptoms_text.split(';')
        final_symptoms.update([s.strip() for s in symptoms if s.strip()])
    
    print(f"Standardized to {len(final_symptoms)} unique symptoms")
    print(f"Top symptoms: {sorted(list(final_symptoms))[:20]}")
    
    # After initial standardization, restrict to canonical vocabulary to avoid long narrative tokens
    CANONICAL = set([
        'Fever','Chills','Headache','Fatigue','Abdominal Pain','Burning Sensation','Frequent Urination',
        'Cough','Nausea','Vomiting','Muscle Pain','Joint Pain','Skin Rash','Dizziness','Chest Pain',
        'Shortness of Breath','Night Sweats','Weight Loss','Blurred Vision','Excessive Thirst',
        'Loss of Appetite','Constipation'
    ])

    def filter_to_canonical(symptoms_text: str) -> str:
        tokens = [s.strip() for s in symptoms_text.split(';') if s.strip()]
        kept = []
        for t in tokens:
            if t in CANONICAL:
                kept.append(t)
            else:
                tl = t.lower()
                # Map common narratives to canonical
                if 'rash' in tl or 'ring' in tl or 'scaly' in tl or 'skin' in tl:
                    kept.append('Skin Rash')
                elif 'urinate' in tl or 'urination' in tl:
                    kept.append('Frequent Urination')
                elif 'thirst' in tl:
                    kept.append('Excessive Thirst')
                elif 'blur' in tl and 'vision' in tl:
                    kept.append('Blurred Vision')
                elif 'pain' in tl and 'abdomen' in tl or 'stomach' in tl:
                    kept.append('Abdominal Pain')
                elif 'short' in tl and 'breath' in tl:
                    kept.append('Shortness of Breath')
                elif 'cough' in tl:
                    kept.append('Cough')
                elif 'fever' in tl:
                    kept.append('Fever')
                elif 'headache' in tl:
                    kept.append('Headache')
                elif 'nausea' in tl:
                    kept.append('Nausea')
                elif 'vomit' in tl:
                    kept.append('Vomiting')
        # Deduplicate
        kept = list(dict.fromkeys([k for k in kept if k in CANONICAL]))
        return '; '.join(kept)

    data['Symptoms'] = data['Symptoms'].apply(filter_to_canonical)

    # Remove rows that ended up empty after filtering
    before = len(data)
    data = data[data['Symptoms'].str.len() > 0]
    after = len(data)
    if after < before:
        print(f"Filtered out {before - after} rows with non-canonical symptoms")

    return data

def create_advanced_features(data):
    """Enhanced feature engineering with medical knowledge"""
    print("🔬 Creating advanced features...")
    
    # Extract all unique symptoms
    symptoms = set()
    for symptom_list in data['Symptoms'].str.split(';'):
        symptoms.update([s.strip() for s in symptom_list if s.strip()])
    
    print(f"Creating features for {len(symptoms)} symptoms...")
    
    # Basic symptom features
    for symptom in symptoms:
        data[f'Symptom_{symptom}'] = data['Symptoms'].apply(
            lambda x: 1 if symptom in str(x) else 0
        )
    
    # Enhanced symptom combinations based on medical knowledge
    symptom_combinations = [
        ('Fever', 'Chills', 'Fever_Chills'),
        ('Fever', 'Abdominal Pain', 'Fever_AbPain'),
        ('Frequent Urination', 'Burning Sensation', 'UTI_Symptoms'),
        ('Cough', 'Fever', 'Respiratory_Infection'),
        ('Headache', 'Fever', 'Systemic_Infection'),
        ('Fatigue', 'Fever', 'Acute_Illness'),
        ('Cough', 'Chest Pain', 'Lower_Respiratory'),
        ('Burning Sensation', 'Fever', 'UTI_Fever'),
        ('Headache', 'Nausea', 'Neurological'),
        ('Fever', 'Muscle Pain', 'Viral_Syndrome'),
        ('Abdominal Pain', 'Nausea', 'GI_Distress'),
        ('Fatigue', 'Dizziness', 'Systemic_Weakness'),
        ('Excessive Thirst', 'Frequent Urination', 'Diabetes_Classic'),
        ('Chest Pain', 'Shortness of Breath', 'Cardiopulmonary'),
        ('Headache', 'Dizziness', 'Hypertensive_Crisis')
    ]
    
    for sym1, sym2, combo_name in symptom_combinations:
        if f'Symptom_{sym1}' in data.columns and f'Symptom_{sym2}' in data.columns:
            data[f'Combo_{combo_name}'] = (
                data[f'Symptom_{sym1}'] & data[f'Symptom_{sym2}']
            ).astype(int)
    
    # System-based symptom scores
    symptom_cols = [col for col in data.columns if col.startswith('Symptom_')]
    data['Total_Symptoms'] = data[symptom_cols].sum(axis=1)
    
    # Fever-related score
    fever_symptoms = ['Symptom_Fever', 'Symptom_Chills', 'Symptom_Night Sweats']
    data['Fever_Score'] = sum(data.get(col, 0) for col in fever_symptoms)
    
    # Respiratory score
    respiratory_symptoms = ['Symptom_Cough', 'Symptom_Chest Pain', 'Symptom_Shortness of Breath']
    data['Respiratory_Score'] = sum(data.get(col, 0) for col in respiratory_symptoms)
    
    # GI score
    gi_symptoms = ['Symptom_Abdominal Pain', 'Symptom_Nausea', 'Symptom_Vomiting', 'Symptom_Loss of Appetite']
    data['GI_Score'] = sum(data.get(col, 0) for col in gi_symptoms)
    
    # Urinary score
    urinary_symptoms = ['Symptom_Frequent Urination', 'Symptom_Burning Sensation']
    data['Urinary_Score'] = sum(data.get(col, 0) for col in urinary_symptoms)
    
    # Neurological score
    neuro_symptoms = ['Symptom_Headache', 'Symptom_Dizziness', 'Symptom_Blurred Vision']
    data['Neuro_Score'] = sum(data.get(col, 0) for col in neuro_symptoms)
    
    # Constitutional symptoms score
    constitutional_symptoms = ['Symptom_Fatigue', 'Symptom_Weight Loss', 'Symptom_Muscle Pain']
    data['Constitutional_Score'] = sum(data.get(col, 0) for col in constitutional_symptoms)
    
    print(f"Created {len([col for col in data.columns if col.startswith(('Symptom_', 'Combo_')) or col.endswith('_Score')])} features")
    
    return data

def preprocess_features(df):
    """Preprocess features and encode labels"""
    print("⚙️ Preprocessing features...")
    
    data = df.copy()
    data = create_advanced_features(data)
    
    # Encode diseases
    le = LabelEncoder()
    data['Disease_encoded'] = le.fit_transform(data['Disease'])
    
    # Select feature columns
    feature_cols = [col for col in data.columns if 
                   col.startswith('Symptom_') or 
                   col.startswith('Combo_') or 
                   col.endswith('_Score') or 
                   col == 'Total_Symptoms']
    
    X = data[feature_cols]
    y = data['Disease_encoded']
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of classes: {len(le.classes_)}")
    print(f"Classes: {list(le.classes_)}")
    
    return X, y, le, data, feature_cols

# ====================== 2. Enhanced Model Architecture ======================

def create_enhanced_disease_model(input_dim, output_dim):
    """Enhanced neural network with attention mechanism"""
    inputs = keras.Input(shape=(input_dim,))
    
    # Feature extraction with batch normalization
    x = layers.Dense(512, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    x = layers.Dense(128, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    
    # Attention mechanism
    attention = layers.Dense(input_dim, activation='softmax')(x)
    attended_input = layers.Multiply()([inputs, attention])
    
    # Combine features
    combined = layers.Concatenate()([x, attended_input])
    
    # Final layers
    x = layers.Dense(64, activation='relu')(combined)
    x = layers.Dropout(0.2)(x)
    
    outputs = layers.Dense(output_dim, activation='softmax')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_ensemble_models(X_train, y_train):
    """Create multiple models for ensemble"""
    models = {}
    
    # Random Forest
    models['rf'] = RandomForestClassifier(
        n_estimators=200, 
        random_state=42, 
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    # Gradient Boosting
    models['gb'] = GradientBoostingClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=6,
        learning_rate=0.1
    )
    
    # Logistic Regression
    models['lr'] = LogisticRegression(
        random_state=42, 
        max_iter=1000,
        C=1.0
    )
    
    # SVM
    models['svm'] = SVC(
        random_state=42,
        probability=True,
        kernel='rbf',
        C=1.0
    )
    
    # Train all models
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
    
    # Create voting classifier
    ensemble = VotingClassifier(
        estimators=[(name, model) for name, model in models.items()],
        voting='soft'
    )
    ensemble.fit(X_train, y_train)
    
    return models, ensemble

# ====================== 3. Enhanced Training & Evaluation ======================

def train_with_advanced_sampling(X, y):
    """Enhanced training with SMOTE and proper validation"""
    print("🎯 Splitting and balancing data...")
    
    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Train set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    print(f"Original class distribution: {Counter(y_train)}")
    
    # Apply SMOTE for balanced training
    smote = SMOTE(random_state=42, k_neighbors=min(3, Counter(y_train).most_common()[-1][1]-1))
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_balanced)
    X_test_scaled = scaler.transform(X_test)
    
    # Compute class weights
    class_weights = compute_class_weight(
        'balanced', 
        classes=np.unique(y_train_balanced), 
        y=y_train_balanced
    )
    class_weights = dict(enumerate(class_weights))
    
    print(f"Training set shape after SMOTE: {X_train_scaled.shape}")
    print(f"Balanced class distribution: {Counter(y_train_balanced)}")
    
    return X_train_scaled, X_test_scaled, y_train_balanced, y_test, scaler, class_weights

def enhanced_prediction_refinement(y_pred_probs, X_test, feature_cols, disease_encoder):
    """Medical knowledge-based prediction refinement"""
    y_pred = np.argmax(y_pred_probs, axis=1)
    confidence_scores = np.max(y_pred_probs, axis=1)
    
    # Disease-specific confidence thresholds
    confidence_thresholds = {
        'Malaria': 0.7,
        'Typhoid': 0.65,
        'Pneumonia': 0.7,
        'Urinary Tract Infection': 0.6,
        'Diabetes': 0.65,
        'Migraine': 0.5,
        'Common Cold': 0.4,
        'Fungal Infection': 0.6,
        'Hypertension': 0.6,
        'Gastritis': 0.6
    }
    
    def get_feature_idx(feature_name):
        try:
            return feature_cols.index(feature_name)
        except ValueError:
            return -1
    
    # Apply medical knowledge rules
    for i in range(len(y_pred)):
        disease = disease_encoder.classes_[y_pred[i]]
        confidence = confidence_scores[i]
        disease_threshold = confidence_thresholds.get(disease, 0.6)
        
        if confidence < disease_threshold:
            # Get symptom indices
            fever_idx = get_feature_idx('Symptom_Fever')
            chills_idx = get_feature_idx('Symptom_Chills')
            cough_idx = get_feature_idx('Symptom_Cough')
            abpain_idx = get_feature_idx('Symptom_Abdominal Pain')
            burning_idx = get_feature_idx('Symptom_Burning Sensation')
            freq_urin_idx = get_feature_idx('Symptom_Frequent Urination')
            headache_idx = get_feature_idx('Symptom_Headache')
            
            # Apply medical rules
            if disease == 'Malaria':
                if (fever_idx == -1 or chills_idx == -1 or 
                    X_test[i, fever_idx] == 0 or X_test[i, chills_idx] == 0):
                    if abpain_idx != -1 and X_test[i, abpain_idx] == 1:
                        try:
                            y_pred[i] = disease_encoder.transform(['Typhoid'])[0]
                        except:
                            pass
                    elif cough_idx != -1 and X_test[i, cough_idx] == 1:
                        try:
                            y_pred[i] = disease_encoder.transform(['Pneumonia'])[0]
                        except:
                            pass
            
            elif disease == 'Urinary Tract Infection':
                if (burning_idx == -1 or freq_urin_idx == -1 or
                    (X_test[i, burning_idx] == 0 and X_test[i, freq_urin_idx] == 0)):
                    if fever_idx != -1 and X_test[i, fever_idx] == 1:
                        try:
                            y_pred[i] = disease_encoder.transform(['Typhoid'])[0]
                        except:
                            pass
                    else:
                        try:
                            y_pred[i] = disease_encoder.transform(['Diabetes'])[0]
                        except:
                            pass
            
            elif disease == 'Pneumonia':
                if cough_idx != -1 and X_test[i, cough_idx] == 0:
                    if (fever_idx != -1 and chills_idx != -1 and
                        X_test[i, fever_idx] == 1 and X_test[i, chills_idx] == 1):
                        try:
                            y_pred[i] = disease_encoder.transform(['Malaria'])[0]
                        except:
                            pass
                    else:
                        try:
                            y_pred[i] = disease_encoder.transform(['Common Cold'])[0]
                        except:
                            pass
    
    return y_pred, confidence_scores

def comprehensive_evaluation(models, ensemble_model, nn_model, X_test, y_test, disease_encoder, feature_cols):
    """Comprehensive evaluation with detailed metrics"""
    results = {}
    
    # Neural Network predictions
    y_pred_probs_nn = nn_model.predict(X_test, verbose=0)
    y_pred_nn, confidence_scores = enhanced_prediction_refinement(
        y_pred_probs_nn, X_test, feature_cols, disease_encoder
    )
    
    # Individual model predictions
    model_predictions = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        model_predictions[name] = y_pred
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'f1_macro': f1_score(y_test, y_pred, average='macro'),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted')
        }
    
    # Ensemble predictions
    y_pred_ensemble = ensemble_model.predict(X_test)
    results['ensemble'] = {
        'accuracy': accuracy_score(y_test, y_pred_ensemble),
        'f1_macro': f1_score(y_test, y_pred_ensemble, average='macro'),
        'f1_weighted': f1_score(y_test, y_pred_ensemble, average='weighted')
    }
    
    # Neural Network results
    results['neural_network'] = {
        'accuracy': accuracy_score(y_test, y_pred_nn),
        'f1_macro': f1_score(y_test, y_pred_nn, average='macro'),
        'f1_weighted': f1_score(y_test, y_pred_nn, average='weighted')
    }
    
    # Combined predictions (ensemble + NN)
    y_pred_combined = []
    for i in range(len(y_test)):
        if confidence_scores[i] > 0.7:
            y_pred_combined.append(y_pred_nn[i])
        else:
            y_pred_combined.append(y_pred_ensemble[i])
    
    y_pred_combined = np.array(y_pred_combined)
    results['combined'] = {
        'accuracy': accuracy_score(y_test, y_pred_combined),
        'f1_macro': f1_score(y_test, y_pred_combined, average='macro'),
        'f1_weighted': f1_score(y_test, y_pred_combined, average='weighted')
    }
    
    return results, y_pred_combined, y_pred_nn, y_pred_ensemble, model_predictions

# ====================== 4. Visualization Functions ======================

def plot_data_analysis(data):
    """Plot data analysis visualizations"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Disease distribution
    disease_counts = data['Disease'].value_counts()
    axes[0,0].bar(range(len(disease_counts)), disease_counts.values)
    axes[0,0].set_title('Disease Distribution', fontweight='bold')
    axes[0,0].set_xlabel('Disease')
    axes[0,0].set_ylabel('Count')
    axes[0,0].set_xticks(range(len(disease_counts)))
    axes[0,0].set_xticklabels(disease_counts.index, rotation=45, ha='right')
    
    # Symptom count distribution
    symptom_counts = data['Total_Symptoms']
    axes[0,1].hist(symptom_counts, bins=20, alpha=0.7)
    axes[0,1].set_title('Symptom Count Distribution', fontweight='bold')
    axes[0,1].set_xlabel('Number of Symptoms')
    axes[0,1].set_ylabel('Frequency')
    
    # System scores
    system_scores = ['Fever_Score', 'Respiratory_Score', 'GI_Score', 'Urinary_Score', 'Neuro_Score']
    system_means = [data[score].mean() for score in system_scores if score in data.columns]
    system_names = [score.replace('_Score', '') for score in system_scores if score in data.columns]
    
    if system_means:
        axes[1,0].bar(system_names, system_means)
        axes[1,0].set_title('Average System Involvement Scores', fontweight='bold')
        axes[1,0].set_ylabel('Average Score')
        axes[1,0].tick_params(axis='x', rotation=45)
    
    # Dataset statistics
    stats_text = f"""Dataset Statistics:
    
Total Samples: {len(data)}
Number of Diseases: {data['Disease'].nunique()}
Average Symptoms per Case: {data['Total_Symptoms'].mean():.1f}
Max Symptoms per Case: {data['Total_Symptoms'].max()}
Min Symptoms per Case: {data['Total_Symptoms'].min()}

Most Common Diseases:
{disease_counts.head(5).to_string()}
    """
    
    axes[1,1].text(0.1, 0.9, stats_text, transform=axes[1,1].transAxes, 
                   fontsize=10, verticalalignment='top', fontfamily='monospace')
    axes[1,1].set_title('Dataset Statistics', fontweight='bold')
    axes[1,1].axis('off')
    
    plt.suptitle('Data Analysis Overview', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('disease_figures/data_analysis.png', bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()

def plot_training_history(history):
    """Plot training accuracy and loss curves"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy plot
    axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0].set_title('Model Training Accuracy and Loss Curves', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Loss plot
    axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('disease_figures/training_history.png', bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()

def plot_confusion_matrix(y_test, y_pred, disease_encoder, title):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d',
                xticklabels=disease_encoder.classes_,
                yticklabels=disease_encoder.classes_,
                cmap='Blues', cbar_kws={'label': 'Count'})
    
    plt.title(f'Confusion Matrix of {title}', fontsize=16, fontweight='bold')
    plt.xlabel('Predicted Disease', fontsize=12)
    plt.ylabel('Actual Disease', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    filename = f"disease_figures/confusion_matrix_{title.lower().replace(' ', '_')}.png"
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()

def plot_classification_metrics(y_test, y_pred, disease_encoder):
    """Plot precision, recall, and F1-score per class"""
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred)
    
    # Create DataFrame for easier plotting
    metrics_df = pd.DataFrame({
        'Disease': disease_encoder.classes_,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'Support': support
    })
    
    # Plot metrics
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Precision
    sns.barplot(data=metrics_df, x='Precision', y='Disease', ax=axes[0,0], palette='viridis')
    axes[0,0].set_title('Precision per Class', fontweight='bold')
    axes[0,0].set_xlim(0, 1)
    
    # Recall
    sns.barplot(data=metrics_df, x='Recall', y='Disease', ax=axes[0,1], palette='plasma')
    axes[0,1].set_title('Recall per Class', fontweight='bold')
    axes[0,1].set_xlim(0, 1)
    
    # F1-Score
    sns.barplot(data=metrics_df, x='F1-Score', y='Disease', ax=axes[1,0], palette='coolwarm')
    axes[1,0].set_title('F1-Score per Class', fontweight='bold')
    axes[1,0].set_xlim(0, 1)
    
    # Support
    sns.barplot(data=metrics_df, x='Support', y='Disease', ax=axes[1,1], palette='Set2')
    axes[1,1].set_title('Support per Class', fontweight='bold')
    
    plt.suptitle('Precision, Recall, and F1-Score per Class', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('disease_figures/classification_metrics.png', bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()
    
    return metrics_df

def plot_model_comparison(results):
    """Plot accuracy comparison across models"""
    models = list(results.keys())
    accuracies = [results[model]['accuracy'] for model in models]
    f1_scores = [results[model]['f1_weighted'] for model in models]
    
    x = np.arange(len(models))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars1 = ax.bar(x - width/2, accuracies, width, label='Accuracy', alpha=0.8)
    bars2 = ax.bar(x + width/2, f1_scores, width, label='F1-Score (Weighted)', alpha=0.8)
    
    ax.set_xlabel('Models', fontweight='bold')
    ax.set_ylabel('Score', fontweight='bold')
    ax.set_title('Accuracy Comparison Across Models', fontsize=16, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([model.replace('_', ' ').title() for model in models], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('disease_figures/model_comparison.png', bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()
    plt.close(fig)

def plot_feature_importance(models, feature_cols):
    """Plot top 15 symptom features by importance"""
    # Get feature importance from Random Forest
    rf_model = models['rf']
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot top 15 features
    top_features = feature_importance.head(15)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=top_features, x='importance', y='feature', palette='viridis')
    plt.title('Top 15 Symptom Features by Importance', fontsize=16, fontweight='bold')
    plt.xlabel('Feature Importance', fontweight='bold')
    plt.ylabel('Features', fontweight='bold')
    
    # Add value labels
    for i, v in enumerate(top_features['importance']):
        plt.text(v + 0.001, i, f'{v:.3f}', va='center')
    
    plt.tight_layout()
    plt.savefig('disease_figures/feature_importance.png', bbox_inches='tight', dpi=300)
    if SHOW_PLOTS:
        plt.show()
    plt.close()
    
    return feature_importance

def create_detailed_report(results, metrics_df, feature_importance, disease_encoder, data):
    """Create detailed evaluation report"""
    report = {
        'dataset_info': {
            'total_samples': len(data),
            'num_diseases': data['Disease'].nunique(),
            'diseases': disease_encoder.classes_.tolist(),
            'avg_symptoms_per_case': float(data['Total_Symptoms'].mean()),
            'disease_distribution': data['Disease'].value_counts().to_dict()
        },
        'model_performance': results,
        'per_class_metrics': metrics_df.to_dict('records'),
        'top_features': feature_importance.head(20).to_dict('records')
    }
    
    # Save report
    with open('disease_reports/evaluation_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Create text report
    with open('disease_reports/evaluation_summary.txt', 'w') as f:
        f.write("DISEASE PREDICTION MODEL EVALUATION REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("DATASET INFORMATION:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Samples: {len(data)}\n")
        f.write(f"Number of Diseases: {data['Disease'].nunique()}\n")
        f.write(f"Average Symptoms per Case: {data['Total_Symptoms'].mean():.1f}\n")
        f.write(f"Diseases: {', '.join(disease_encoder.classes_)}\n\n")
        
        f.write("MODEL PERFORMANCE SUMMARY:\n")
        f.write("-" * 30 + "\n")
        for model, metrics in results.items():
            f.write(f"{model.upper()}:\n")
            f.write(f"  Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"  F1-Score (Macro): {metrics['f1_macro']:.4f}\n")
            f.write(f"  F1-Score (Weighted): {metrics['f1_weighted']:.4f}\n\n")
        
        f.write("PER-CLASS PERFORMANCE:\n")
        f.write("-" * 25 + "\n")
        for _, row in metrics_df.iterrows():
            f.write(f"{row['Disease']}:\n")
            f.write(f"  Precision: {row['Precision']:.4f}\n")
            f.write(f"  Recall: {row['Recall']:.4f}\n")
            f.write(f"  F1-Score: {row['F1-Score']:.4f}\n")
            f.write(f"  Support: {row['Support']}\n\n")
        
        f.write("TOP 10 MOST IMPORTANT FEATURES:\n")
        f.write("-" * 35 + "\n")
        for i, (_, row) in enumerate(feature_importance.head(10).iterrows(), 1):
            f.write(f"{i:2d}. {row['feature']}: {row['importance']:.4f}\n")

# ====================== 5. Main Training Pipeline ======================

def main():
    """Main training pipeline"""
    print("🚀 Starting Enhanced Disease Prediction Model Training with Real Data...")
    create_directories()
    
    # Load real dataset
    raw_df = load_real_dataset()
    
    # Clean and preprocess data
    cleaned_df = clean_and_preprocess_data(raw_df)
    standardized_df = standardize_symptoms(cleaned_df)
    
    # Create features
    X, y, disease_encoder, processed_data, feature_cols = preprocess_features(standardized_df)
    
    print(f"\nFeatures created: {len(feature_cols)}")
    print(f"Disease classes: {list(disease_encoder.classes_)}")
    print(f"Dataset shape: {X.shape}")
    
    # Plot data analysis
    plot_data_analysis(processed_data)
    
    # Train with advanced sampling
    X_train, X_test, y_train, y_test, scaler, class_weights = train_with_advanced_sampling(X, y)
    
    # Train Neural Network
    print("\n🧠 Training Neural Network...")
    nn_model = create_enhanced_disease_model(X_train.shape[1], len(disease_encoder.classes_))
    
    callbacks_list = [
        callbacks.EarlyStopping(patience=20, restore_best_weights=True, monitor='val_accuracy'),
        callbacks.ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-6),
        callbacks.ModelCheckpoint('disease_models/best_model.h5', save_best_only=True, monitor='val_accuracy')
    ]
    
    history = nn_model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=100,
        batch_size=32,
        class_weight=class_weights,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Train ensemble models
    print("\n🎯 Training Ensemble Models...")
    models, ensemble_model = create_ensemble_models(X_train, y_train)
    
    # Comprehensive evaluation
    print("\n📊 Comprehensive Evaluation...")
    results, y_pred_combined, y_pred_nn, y_pred_ensemble, model_predictions = comprehensive_evaluation(
        models, ensemble_model, nn_model, X_test, y_test, disease_encoder, feature_cols
    )
    
    # Generate all visualizations
    print("\n📈 Generating Visualizations...")
    
    # 1. Training curves
    plot_training_history(history)
    
    # 2. Confusion matrix for neural network
    plot_confusion_matrix(y_test, y_pred_nn, disease_encoder, "Deep Neural Network Predictions")
    
    # 3. Classification metrics
    metrics_df = plot_classification_metrics(y_test, y_pred_combined, disease_encoder)
    
    # 4. Model comparison
    plot_model_comparison(results)
    
    # 5. Feature importance
    feature_importance = plot_feature_importance(models, feature_cols)
    
    # Create detailed report
    create_detailed_report(results, metrics_df, feature_importance, disease_encoder, processed_data)
    
    # Save models and preprocessors
    print("\n💾 Saving Models...")
    nn_model.save('disease_models/enhanced_disease_model.h5')
    
    with open('disease_models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    with open('disease_models/label_encoder.pkl', 'wb') as f:
        pickle.dump(disease_encoder, f)
    
    with open('disease_models/ensemble_model.pkl', 'wb') as f:
        pickle.dump(ensemble_model, f)
    
    with open('disease_models/feature_columns.pkl', 'wb') as f:
        pickle.dump(feature_cols, f)
    
    with open('disease_models/individual_models.pkl', 'wb') as f:
        pickle.dump(models, f)
    
    # Save processed dataset
    processed_data.to_csv('disease_reports/processed_dataset.csv', index=False)
    
    # Print final results
    print("\n✅ Training Complete!")
    print("\nFINAL RESULTS:")
    print("=" * 50)
    for model, metrics in results.items():
        print(f"{model.upper()}:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  F1-Score (Macro): {metrics['f1_macro']:.4f}")
        print(f"  F1-Score (Weighted): {metrics['f1_weighted']:.4f}")
        print()
    
    print("All models, visualizations, and reports have been saved!")
    print("Check the 'disease_figures' folder for visualizations.")
    print("Check the 'disease_reports' folder for detailed reports.")
    print("Check the 'disease_models' folder for trained models.")

if __name__ == "__main__":
    main()


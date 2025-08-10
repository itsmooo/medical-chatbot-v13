#!/usr/bin/env python3
"""
FIXED Medical Disease Prediction Model Training
- Implements comprehensive anti-overfitting measures
- Uses realistic feature engineering
- Includes data leakage checks
- Provides proper validation
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers, callbacks
import pickle
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Create directories
os.makedirs('disease_models', exist_ok=True)
os.makedirs('disease_reports', exist_ok=True)
os.makedirs('disease_figures', exist_ok=True)

def load_local_medical_dataset(filepath='medical_dataset.csv'):
    """Load the medical dataset from a local CSV file with validation"""
    print("📥 Loading and validating local medical dataset...")
    
    try:
        df = pd.read_csv(filepath)
        
        # Basic validation
        if len(df) < 100:
            raise ValueError("Dataset too small (needs at least 100 samples)")
        if 'Disease' not in df.columns or 'Symptoms' not in df.columns:
            raise ValueError("Missing required columns (Disease, Symptoms)")
        
        print(f"✅ Dataset loaded successfully from {filepath}!")
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nSample data preview:")
        print(df.head(3))
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None

def clean_and_preprocess_data(df):
    """Clean and preprocess the medical dataset with aggressive deduplication"""
    print("\n🧹 Cleaning and preprocessing data with anti-overfitting measures...")
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.title()
    
    # Check for required columns
    required_cols = ['Disease', 'Symptoms', 'Precautions']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"❌ Missing required columns: {missing_cols}")
        return None
    
    # Initial count for reporting
    initial_count = len(df)
    
    # Remove duplicates based on symptoms+disease pairs
    df = df.drop_duplicates(subset=['Disease', 'Symptoms'])
    
    # More aggressive deduplication - normalize text first
    df['Symptoms_Normalized'] = (
        df['Symptoms']
        .str.lower()
        .str.replace(r'[^\w\s]', '')  # Remove punctuation
        .str.replace(r'\s+', ' ')      # Normalize whitespace
        .str.strip()
    )
    
    # Remove near-duplicates after normalization
    df = df.drop_duplicates(subset=['Disease', 'Symptoms_Normalized'])
    df = df.drop(columns=['Symptoms_Normalized'])
    
    # Remove rows with missing critical data
    df = df.dropna(subset=['Disease', 'Symptoms'])
    
    # Clean text data more thoroughly
    text_columns = ['Disease', 'Symptoms', 'Precautions']
    for col in text_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r'\s+', ' ', regex=True)
            )
    
    # Filter out diseases with too few samples (less than 5)
    disease_counts = df['Disease'].value_counts()
    valid_diseases = disease_counts[disease_counts >= 5].index
    df = df[df['Disease'].isin(valid_diseases)]
    
    # Report cleaning results
    print(f"\nData cleaning report:")
    print(f"- Removed {initial_count - len(df)} rows ({(initial_count - len(df))/initial_count*100:.1f}%)")
    print(f"- Final dataset shape: {df.shape}")
    print(f"- Remaining diseases: {len(df['Disease'].unique())}")
    print("\nDisease distribution after cleaning:")
    print(df['Disease'].value_counts().head())
    
    return df

def check_for_data_leakage(df_train, df_test):
    """Check if test data appears in training data (normalized comparison)"""
    print("\n🔍 Checking for data leakage...")
    
    def normalize_text(s):
        return (
            s.str.lower()
            .str.replace(r'[^\w\s]', '')
            .str.replace(r'\s+', ' ')
            .str.strip()
        )
    
    train_symptoms = set(normalize_text(df_train['Symptoms']))
    test_symptoms = set(normalize_text(df_test['Symptoms']))
    
    overlap = train_symptoms.intersection(test_symptoms)
    overlap_percent = len(overlap) / len(test_symptoms) * 100
    
    print(f"Data Leakage Check Results:")
    print(f"- Unique train symptoms: {len(train_symptoms)}")
    print(f"- Unique test symptoms: {len(test_symptoms)}")
    print(f"- Overlapping symptoms: {len(overlap)} ({overlap_percent:.2f}%)")
    
    if overlap_percent > 5:
        print("⚠️ WARNING: Significant data leakage detected!")
        print("Recommendation: Review dataset for duplicate/near-duplicate entries")
    else:
        print("✅ No significant data leakage detected")
    
    return overlap_percent

def create_realistic_features(df):
    """Create features with strong anti-overfitting measures"""
    print("\n🔬 Creating realistic features with anti-overfitting protection...")
    
    # More conservative TF-IDF settings
    vectorizer = TfidfVectorizer(
        max_features=500,  # Reduced from 1000 to prevent overfitting
        stop_words='english',
        ngram_range=(1, 1),  # Only unigrams (no bigrams)
        min_df=5,  # Must appear in at least 5 documents
        max_df=0.7,  # Must not appear in more than 70% of documents
        lowercase=True,
        strip_accents='ascii',
        sublinear_tf=True  # Use sublinear TF scaling
    )
    
    # Fit vectorizer on symptoms
    print("\nFitting vectorizer with strict parameters...")
    X = vectorizer.fit_transform(df['Symptoms'])
    
    # Encode disease labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['Disease'])
    
    # Feature statistics
    print("\nFeature engineering report:")
    print(f"- Feature matrix shape: {X.shape}")
    print(f"- Number of classes: {len(label_encoder.classes_)}")
    print(f"- Average non-zero features per sample: {X.nnz / X.shape[0]:.1f}")
    
    # Check feature distribution
    nonzero_counts = np.diff(X.indptr)
    plt.figure(figsize=(10, 4))
    plt.hist(nonzero_counts, bins=50)
    plt.title('Distribution of Non-Zero Features per Sample')
    plt.xlabel('Number of Features')
    plt.ylabel('Frequency')
    plt.savefig('disease_figures/feature_distribution.png')
    plt.close()
    
    return X, y, vectorizer, label_encoder

def create_anti_overfitting_model(input_dim, output_dim):
    """Create neural network with strong regularization"""
    print("\n🧠 Creating anti-overfitting neural network architecture...")
    
    model = keras.Sequential([
        # Input layer with dropout and strong regularization
        layers.Dense(64, activation='relu', input_shape=(input_dim,),
                    kernel_regularizer=regularizers.l2(0.1),  # Strong L2
                    activity_regularizer=regularizers.l1(0.05)),  # L1 regularization
        layers.BatchNormalization(),
        layers.Dropout(0.6),  # High dropout rate
        
        # Hidden layer with even stronger regularization
        layers.Dense(32, activation='relu',
                    kernel_regularizer=regularizers.l2(0.1),
                    activity_regularizer=regularizers.l1(0.05)),
        layers.BatchNormalization(),
        layers.Dropout(0.7),  # Very high dropout
        
        # Output layer
        layers.Dense(output_dim, activation='softmax')
    ])
    
    # Use very low learning rate with AdamW optimizer
    optimizer = keras.optimizers.AdamW(learning_rate=0.0001, weight_decay=0.01)
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Model architecture summary:")
    model.summary()
    
    return model

def train_with_proper_validation(X, y, df):
    """Train/val/test split with stratification and leakage checks"""
    print("\n🎯 Creating proper validation splits with leakage prevention...")
    
    # Initial split (80% train+val, 20% test)
    X_temp, X_test, y_temp, y_test, df_temp, df_test = train_test_split(
        X, y, df, 
        test_size=0.2, 
        random_state=42, 
        stratify=y
    )
    
    # Secondary split (75% train, 25% val)
    X_train, X_val, y_train, y_val, df_train, df_val = train_test_split(
        X_temp, y_temp, df_temp,
        test_size=0.25, 
        random_state=42, 
        stratify=y_temp
    )
    
    # Check for data leakage
    leakage_percent = check_for_data_leakage(df_train, df_test)
    
    # Compute class weights to handle imbalance
    class_weights = compute_class_weight(
        'balanced', 
        classes=np.unique(y_train), 
        y=y_train
    )
    class_weight_dict = dict(enumerate(class_weights))
    
    # Dataset statistics
    print("\nDataset split statistics:")
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples") 
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Class weights: {class_weight_dict}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test, df_train, df_val, df_test, class_weight_dict

def train_ensemble_models(X_train, y_train, X_val, y_val, class_weight_dict):
    """Train ensemble of models with strong regularization"""
    print("\n🎯 Training ensemble models with anti-overfitting measures...")
    
    models = {}
    
    # Random Forest with strict parameters
    rf = RandomForestClassifier(
        n_estimators=30,  # Reduced from 50
        max_depth=5,      # Very shallow trees
        min_samples_split=20,  # High value prevents overfitting
        min_samples_leaf=10,   # High value prevents overfitting
        max_features=0.3,  # Fewer features per split
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    models['random_forest'] = rf
    
    # Logistic Regression with very strong regularization
    lr = LogisticRegression(
        C=0.01,  # Very strong regularization
        penalty='l2',
        solver='liblinear',
        random_state=42,
        class_weight='balanced',
        max_iter=1000
    )
    models['logistic_regression'] = lr
    
    # SVM with linear kernel and regularization
    svm = SVC(
        C=0.01,  # Strong regularization
        kernel='linear',  # Linear kernel only
        probability=True,
        random_state=42,
        class_weight='balanced'
    )
    models['svm'] = svm
    
    # Naive Bayes with smoothing
    nb = MultinomialNB(alpha=2.0)  # Increased smoothing
    models['naive_bayes'] = nb
    
    # Train all models with cross-validation
    trained_models = {}
    for name, model in models.items():
        print(f"\nTraining {name} with cross-validation...")
        
        # Use 5-fold cross-validation
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
            scoring='accuracy',
            n_jobs=-1
        )
        
        # Now fit on full training set
        model.fit(X_train, y_train)
        
        # Validate on validation set
        val_score = model.score(X_val, y_val)
        train_score = model.score(X_train, y_train)
        
        print(f"{name} performance:")
        print(f"- CV scores: {cv_scores}")
        print(f"- Mean CV accuracy: {np.mean(cv_scores):.4f}")
        print(f"- Training accuracy: {train_score:.4f}")
        print(f"- Validation accuracy: {val_score:.4f}")
        
        # Overfitting check
        if train_score - val_score > 0.15:
            print(f"⚠️ WARNING: {name} may be overfitting!")
        elif train_score - val_score < 0.05:
            print("✅ Good generalization")
        
        trained_models[name] = model
    
    # Create voting classifier with weights based on validation performance
    print("\nCreating weighted ensemble...")
    ensemble = VotingClassifier(
        estimators=[(name, model) for name, model in trained_models.items()],
        voting='soft',
        weights=[model.score(X_val, y_val) for model in trained_models.values()]  # Weight by val performance
    )
    ensemble.fit(X_train, y_train)
    
    return trained_models, ensemble

def train_neural_network(X_train, y_train, X_val, y_val, class_weight_dict, num_classes):
    """Train neural network with early stopping and regularization"""
    print("\n🧠 Training neural network with strong regularization...")
    
    # Convert sparse matrices to dense for neural network
    X_train_dense = X_train.toarray()
    X_val_dense = X_val.toarray()
    
    # Create model
    model = create_anti_overfitting_model(X_train_dense.shape[1], num_classes)
    
    # Callbacks for early stopping and learning rate reduction
    callbacks_list = [
        callbacks.EarlyStopping(
            patience=15,  # Increased patience
            restore_best_weights=True,
            monitor='val_loss',
            min_delta=0.001,  # Minimum change to qualify as improvement
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            'disease_models/best_nn_model.h5',
            save_best_only=True,
            monitor='val_loss',
            mode='min'
        )
    ]
    
    # Train with validation
    print("\nStarting neural network training...")
    history = model.fit(
        X_train_dense, y_train,
        validation_data=(X_val_dense, y_val),
        epochs=200,  # Will stop early due to callback
        batch_size=32,
        class_weight=class_weight_dict,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Plot training history
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Accuracy Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Loss Over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.savefig('disease_figures/training_history.png')
    plt.close()
    
    return model, history

def evaluate_models(models, ensemble, nn_model, X_test, y_test, label_encoder):
    """Comprehensive model evaluation with multiple metrics"""
    print("\n📊 Comprehensive model evaluation on test set...")
    
    results = {}
    reports = {}
    confusion_matrices = {}
    
    # Convert test data for neural network
    X_test_dense = X_test.toarray()
    
    def evaluate_model(name, model, X, is_nn=False):
        if is_nn:
            y_pred_proba = model.predict(X, verbose=0)
            y_pred = np.argmax(y_pred_proba, axis=1)
        else:
            y_pred = model.predict(X)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, 
                                     target_names=label_encoder.classes_,
                                     output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = accuracy
        reports[name] = report
        confusion_matrices[name] = cm
        
        print(f"\n{name} Evaluation:")
        print(f"- Accuracy: {accuracy:.4f}")
        print(f"- Macro Avg F1: {report['macro avg']['f1-score']:.4f}")
        print(f"- Weighted Avg F1: {report['weighted avg']['f1-score']:.4f}")
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', 
                   xticklabels=label_encoder.classes_,
                   yticklabels=label_encoder.classes_,
                   cmap='Blues')
        plt.title(f'Confusion Matrix - {name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'disease_figures/confusion_matrix_{name}.png')
        plt.close()
    
    # Evaluate individual models
    for name, model in models.items():
        evaluate_model(name, model, X_test)
    
    # Evaluate ensemble
    evaluate_model('ensemble', ensemble, X_test)
    
    # Evaluate neural network
    evaluate_model('neural_network', nn_model, X_test_dense, is_nn=True)
    
    # Print best model info
    best_model_name = max(results, key=results.get)
    best_accuracy = results[best_model_name]
    
    print("\n" + "="*60)
    print("FINAL MODEL COMPARISON")
    print("="*60)
    for name, acc in results.items():
        print(f"{name:20}: {acc:.4f} {'(BEST)' if name == best_model_name else ''}")
    
    print("\nBest model:", best_model_name)
    print("Best accuracy:", f"{best_accuracy:.4f}")
    
    # Realistic accuracy assessment
    if best_accuracy > 0.95:
        print("\n⚠️ WARNING: Accuracy still suspiciously high - possible issues:")
        print("- Data leakage may still exist")
        print("- Features may be too predictive")
        print("- Test set may not be representative")
    elif best_accuracy < 0.6:
        print("\n⚠️ WARNING: Accuracy quite low - possible issues:")
        print("- Dataset may be too noisy")
        print("- Features may not be informative enough")
        print("- Classes may be too similar")
    else:
        print("\n✅ Accuracy in realistic range for medical diagnosis")
    
    return results, reports, confusion_matrices

def extract_precautions_mapping(df):
    """Extract and clean precautions for each disease"""
    print("\n💊 Extracting and cleaning precautions mapping...")
    
    precautions_map = {}
    
    for disease in df['Disease'].unique():
        disease_data = df[df['Disease'] == disease]
        
        # Collect all precautions for this disease
        all_precautions = []
        for precaution_text in disease_data['Precautions'].dropna():
            if precaution_text.strip():
                # Split precautions by common delimiters and clean
                precautions = re.split(r'[;,.]+', precaution_text)
                precautions = [
                    p.strip().capitalize()
                    for p in precautions 
                    if p.strip() and len(p.strip()) > 10  # Filter very short ones
                ]
                all_precautions.extend(precautions)
        
        # Remove duplicates and keep most common ones
        if all_precautions:
            precaution_counts = Counter(all_precautions)
            # Keep top 3-5 most common unique precautions
            top_precautions = []
            seen = set()
            for p, count in precaution_counts.most_common():
                simplified = p.lower().strip()
                if simplified not in seen and len(top_precautions) < 5:
                    seen.add(simplified)
                    top_precautions.append(p)
            precautions_map[disease] = top_precautions
        else:
            # Fallback generic precautions
            precautions_map[disease] = [
                "Consult a healthcare professional",
                "Follow prescribed medications",
                "Maintain proper nutrition and rest",
                "Monitor symptoms regularly"
            ]
    
    print(f"Extracted precautions for {len(precautions_map)} diseases")
    print("\nSample precautions mapping:")
    for disease, pre in list(precautions_map.items())[:3]:
        print(f"{disease}: {pre}")
    
    return precautions_map

def save_models_and_components(models, ensemble, nn_model, vectorizer, label_encoder, precautions_map):
    """Save all trained models and components with versioning"""
    print("\n💾 Saving models and components with versioning...")
    
    import time
    timestamp = int(time.time())
    version_dir = f"disease_models/v{timestamp}"
    os.makedirs(version_dir, exist_ok=True)
    
    # Save individual models
    with open(f'{version_dir}/individual_models.pkl', 'wb') as f:
        pickle.dump(models, f)
    
    # Save ensemble model
    with open(f'{version_dir}/ensemble_model.pkl', 'wb') as f:
        pickle.dump(ensemble, f)
    
    # Save neural network
    nn_model.save(f'{version_dir}/neural_network_model.h5')
    
    # Save preprocessing components
    with open(f'{version_dir}/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open(f'{version_dir}/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # Save precautions mapping
    with open(f'{version_dir}/precautions_mapping.pkl', 'wb') as f:
        pickle.dump(precautions_map, f)
    
    # Create symlink to latest
    if os.path.exists('disease_models/latest'):
        os.remove('disease_models/latest')
    os.symlink(f'v{timestamp}', 'disease_models/latest')
    
    print(f"✅ All models and components saved to {version_dir}!")
    print(f"Symlinked 'latest' to v{timestamp}")

def main():
    """Main training pipeline with comprehensive validation"""
    print("\n" + "="*60)
    print("MEDICAL DISEASE PREDICTION TRAINING WITH ANTI-OVERFITTING")
    print("="*60)
    
    # Load local dataset
    df = load_local_medical_dataset('data/medical_chatbot_dataset-R -.csv')
    if df is None:
        print("❌ Failed to load dataset. Please ensure 'data/medical_chatbot_dataset-R -.csv' exists.")
        return
    
    # Clean and preprocess
    df_clean = clean_and_preprocess_data(df)
    if df_clean is None:
        print("❌ Failed to preprocess dataset. Exiting.")
        return
    
    # Create features
    X, y, vectorizer, label_encoder = create_realistic_features(df_clean)
    
    # Split data properly
    (X_train, X_val, X_test, 
     y_train, y_val, y_test,
     df_train, df_val, df_test,
     class_weight_dict) = train_with_proper_validation(X, y, df_clean)
    
    # Train ensemble models
    models, ensemble = train_ensemble_models(X_train, y_train, X_val, y_val, class_weight_dict)
    
    # Train neural network
    nn_model, history = train_neural_network(
        X_train, y_train, X_val, y_val, 
        class_weight_dict, len(label_encoder.classes_)
    )
    
    # Evaluate all models
    results, reports, confusion_matrices = evaluate_models(
        models, ensemble, nn_model, X_test, y_test, label_encoder)
    
    # Extract precautions from dataset
    precautions_map = extract_precautions_mapping(df_clean)
    
    # Save everything
    save_models_and_components(
        models, ensemble, nn_model, 
        vectorizer, label_encoder, precautions_map)
    
    # Final report
    print("\n" + "="*60)
    print("TRAINING COMPLETE - COMPREHENSIVE VALIDATION")
    print("="*60)
    print("✅ Applied multiple anti-overfitting measures:")
    print("   - Aggressive data cleaning and deduplication")
    print("   - Conservative feature engineering")
    print("   - Strong regularization in all models")
    print("   - Proper train/val/test split with stratification")
    print("   - Cross-validation for all models")
    print("   - Early stopping and learning rate reduction")
    print("   - Data leakage checks")
    
    best_model = max(results, key=results.get)
    best_acc = results[best_model]
    
    print(f"\nBest model: {best_model} (accuracy: {best_acc:.4f})")
    
    if best_acc > 0.95:
        print("\n⚠️ WARNING: Accuracy still very high - possible actions:")
        print("- Review dataset for hidden data leakage")
        print("- Make feature engineering even more conservative")
        print("- Collect more diverse data samples")
    elif best_acc < 0.6:
        print("\n⚠️ WARNING: Accuracy quite low - possible actions:")
        print("- Review data quality and labeling")
        print("- Consider more sophisticated features")
        print("- Collect more training data")
    else:
        print("\n✅ Achieved realistic accuracy for medical diagnosis")
    
    print("\nAll models and components saved in disease_models/latest/")
    print("Ready for deployment!")

if __name__ == "__main__":
    main()
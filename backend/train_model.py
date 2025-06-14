import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_preprocess_data(file_path):
    """Load and preprocess the dataset."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded dataset with {len(df)} entries")
        
        # Assuming the CSV has columns: Symptoms, Disease, Precautions
        # Combine symptoms into a single string if they're in separate columns
        if isinstance(df['Symptoms'].iloc[0], str):
            symptoms = df['Symptoms']
        else:
            symptoms = df['Symptoms'].apply(lambda x: ' '.join(x.split(',')))
        
        return symptoms, df['Disease']
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def train_model(symptoms, diseases):
    """Train the disease prediction model."""
    try:
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            symptoms, diseases, test_size=0.2, random_state=42
        )
        
        # Create and fit the TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)
        
        # Train the model
        model = LogisticRegression(
            max_iter=1000,
            C=1.0,
            class_weight='balanced'
        )
        model.fit(X_train_tfidf, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test_tfidf)
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred))
        
        return model, vectorizer
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

def save_model_and_vectorizer(model, vectorizer, model_path, vectorizer_path):
    """Save the trained model and vectorizer."""
    try:
        joblib.dump(model, model_path)
        joblib.dump(vectorizer, vectorizer_path)
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Vectorizer saved to {vectorizer_path}")
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        raise

def main():
    try:
        # Load and preprocess data
        symptoms, diseases = load_and_preprocess_data('data/medical_chatbot_dataset.csv')
        
        # Train model
        model, vectorizer = train_model(symptoms, diseases)
        
        # Save model and vectorizer
        save_model_and_vectorizer(
            model,
            vectorizer,
            'models/disease_predictor.pkl',
            'models/tfidf_vectorizer.pkl'
        )
        
        logger.info("Model training completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
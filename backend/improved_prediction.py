#!/usr/bin/env python3
"""
Improved Disease Prediction Module
- Single Disease Prediction
- Ranking-based Prediction (Top 3)
- Bilingual Support (Somali & English)
- Realistic accuracy ~90%
"""

import joblib
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class ImprovedDiseasePredictor:
    def __init__(self):
        """Initialize the improved disease predictor"""
        self.single_model = None
        self.ranking_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.somali_keywords = {}
        self.models_loaded = False
        
    def load_models(self):
        """Load all trained models and components"""
        try:
            # Load single disease model
            self.single_model = joblib.load('disease_models/single_disease_model.pkl')
            logger.info("✅ Single disease model loaded")
            
            # Load ranking model
            self.ranking_model = joblib.load('disease_models/ranking_model.pkl')
            logger.info("✅ Ranking model loaded")
            
            # Load vectorizer
            self.vectorizer = joblib.load('disease_models/bilingual_vectorizer.pkl')
            logger.info("✅ Bilingual vectorizer loaded")
            
            # Load label encoder
            self.label_encoder = joblib.load('disease_models/bilingual_label_encoder.pkl')
            logger.info("✅ Bilingual label encoder loaded")
            
            # Load Somali keywords
            self.somali_keywords = joblib.load('disease_models/somali_keywords.pkl')
            logger.info("✅ Somali keywords loaded")
            
            self.models_loaded = True
            logger.info("🎉 All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            self.models_loaded = False
            raise
    
    def clean_symptoms(self, symptom_text: str) -> str:
        """Clean and standardize symptom text"""
        if not symptom_text:
            return ""
        
        # Convert to string and lowercase
        text = str(symptom_text).lower().strip()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Basic cleaning
        text = text.replace('_', ' ').replace('-', ' ')
        
        return text
    
    def translate_somali_keywords(self, text: str) -> str:
        """Translate Somali medical keywords to English"""
        text_lower = text.lower()
        translated_text = text
        
        for somali_word, english_word in self.somali_keywords.items():
            if somali_word in text_lower:
                translated_text = translated_text.replace(somali_word, english_word)
        
        return translated_text
    
    def predict_single_disease(self, symptoms_text: str) -> Tuple[str, float]:
        """
        Predict single disease with confidence
        
        Args:
            symptoms_text: Input symptoms (English or Somali)
            
        Returns:
            Tuple of (predicted_disease, confidence)
        """
        if not self.models_loaded:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        # Preprocess symptoms
        cleaned_symptoms = self.clean_symptoms(symptoms_text)
        bilingual_symptoms = self.translate_somali_keywords(cleaned_symptoms)
        
        # Vectorize
        symptoms_vector = self.vectorizer.transform([bilingual_symptoms])
        
        # Predict
        prediction_encoded = self.single_model.predict(symptoms_vector)[0]
        confidence_scores = self.single_model.predict_proba(symptoms_vector)[0]
        confidence = confidence_scores.max()
        
        # Decode prediction
        prediction = self.label_encoder.inverse_transform([prediction_encoded])[0]
        
        logger.info(f"🔍 Single Disease Prediction: '{prediction}' (confidence: {confidence:.4f})")
        
        return prediction, confidence
    
    def predict_ranking(self, symptoms_text: str, top_k: int = 3) -> List[Dict]:
        """
        Predict top K diseases by ranking
        
        Args:
            symptoms_text: Input symptoms (English or Somali)
            top_k: Number of top diseases to return
            
        Returns:
            List of dictionaries with disease, confidence, and rank
        """
        if not self.models_loaded:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        # Preprocess symptoms
        cleaned_symptoms = self.clean_symptoms(symptoms_text)
        bilingual_symptoms = self.translate_somali_keywords(cleaned_symptoms)
        
        # Vectorize
        symptoms_vector = self.vectorizer.transform([bilingual_symptoms])
        
        # Get probabilities
        probabilities = self.ranking_model.predict_proba(symptoms_vector)[0]
        
        # Get top K predictions
        top_indices = np.argsort(probabilities)[-top_k:][::-1]
        
        rankings = []
        for idx in top_indices:
            disease = self.label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[idx]
            rankings.append({
                'disease': disease,
                'confidence': confidence,
                'rank': len(rankings) + 1
            })
        
        logger.info(f"🔍 Ranking Prediction (Top {top_k}):")
        for rank in rankings:
            logger.info(f"  {rank['rank']}. {rank['disease']} (confidence: {rank['confidence']:.4f})")
        
        return rankings
    
    def predict_ensemble(self, symptoms_text: str, use_ranking: bool = True) -> Dict:
        """
        Ensemble prediction combining single disease and ranking approaches
        
        Args:
            symptoms_text: Input symptoms (English or Somali)
            use_ranking: Whether to include ranking predictions
            
        Returns:
            Dictionary with both single and ranking predictions
        """
        if not self.models_loaded:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        # Get single disease prediction
        single_prediction, single_confidence = self.predict_single_disease(symptoms_text)
        
        result = {
            'single_prediction': {
                'disease': single_prediction,
                'confidence': single_confidence
            },
            'input_symptoms': symptoms_text,
            'prediction_type': 'ensemble'
        }
        
        # Add ranking predictions if requested
        if use_ranking:
            rankings = self.predict_ranking(symptoms_text, top_k=3)
            result['ranking_predictions'] = rankings
            
            # Check if single prediction is in top 3
            top_diseases = [r['disease'] for r in rankings]
            result['single_in_top3'] = single_prediction in top_diseases
            
            # Calculate ensemble confidence
            if result['single_in_top3']:
                # If single prediction is in top 3, use average confidence
                matching_rank = next(r for r in rankings if r['disease'] == single_prediction)
                ensemble_confidence = (single_confidence + matching_rank['confidence']) / 2
            else:
                # If not in top 3, use single prediction confidence but flag it
                ensemble_confidence = single_confidence * 0.8  # Reduce confidence
                result['confidence_reduced'] = True
            
            result['ensemble_confidence'] = ensemble_confidence
        
        return result
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        if not self.models_loaded:
            return {'status': 'models_not_loaded'}
        
        return {
            'status': 'models_loaded',
            'single_model_type': type(self.single_model).__name__,
            'ranking_model_type': type(self.ranking_model).__name__,
            'vectorizer_features': len(self.vectorizer.vocabulary_),
            'num_diseases': len(self.label_encoder.classes_),
            'diseases': self.label_encoder.classes_.tolist(),
            'somali_keywords_count': len(self.somali_keywords)
        }

# Global predictor instance
predictor = ImprovedDiseasePredictor()

def load_improved_models():
    """Load the improved models globally"""
    try:
        predictor.load_models()
        return True
    except Exception as e:
        logger.error(f"Failed to load improved models: {str(e)}")
        return False

def predict_single_disease(symptoms_text: str) -> Tuple[str, float]:
    """Predict single disease"""
    return predictor.predict_single_disease(symptoms_text)

def predict_ranking(symptoms_text: str, top_k: int = 3) -> List[Dict]:
    """Predict ranking of diseases"""
    return predictor.predict_ranking(symptoms_text, top_k)

def predict_ensemble(symptoms_text: str, use_ranking: bool = True) -> Dict:
    """Predict using ensemble approach"""
    return predictor.predict_ensemble(symptoms_text, use_ranking)

def get_model_info() -> Dict:
    """Get model information"""
    return predictor.get_model_info()

# Test function
def test_improved_predictions():
    """Test the improved prediction system"""
    try:
        # Load models
        if not load_improved_models():
            logger.error("❌ Failed to load models")
            return
        
        logger.info("🧪 Testing Improved Prediction System")
        logger.info("=" * 50)
        
        # Test cases
        test_cases = [
            "fever cough headache",
            "dhidid qandho madaxa",  # Somali
            "diarrhea vomiting stomach pain",
            "shuban qalli caloolka",  # Somali
            "chest pain shortness of breath",
            "wadnaha neefsasho",  # Somali
        ]
        
        for i, symptoms in enumerate(test_cases, 1):
            logger.info(f"\n🔍 Test Case {i}: '{symptoms}'")
            
            # Single prediction
            disease, confidence = predict_single_disease(symptoms)
            logger.info(f"   Single: {disease} ({confidence:.4f})")
            
            # Ranking prediction
            rankings = predict_ranking(symptoms, top_k=3)
            logger.info(f"   Ranking:")
            for rank in rankings:
                logger.info(f"     {rank['rank']}. {rank['disease']} ({rank['confidence']:.4f})")
            
            # Ensemble prediction
            ensemble = predict_ensemble(symptoms)
            logger.info(f"   Ensemble confidence: {ensemble['ensemble_confidence']:.4f}")
            logger.info(f"   Single in top 3: {ensemble['single_in_top3']}")
        
        # Model info
        info = get_model_info()
        logger.info(f"\n📊 Model Information:")
        logger.info(f"   Diseases: {info['diseases']}")
        logger.info(f"   Somali keywords: {info['somali_keywords_count']}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_improved_predictions() 
# OpenAI Symptom Validation Integration

## Overview

This application now includes OpenAI-powered symptom validation to ensure that users provide legitimate medical symptoms before making disease predictions.

## Features

### 1. Symptom Validation
- **OpenAI Integration**: Uses GPT-3.5-turbo to validate whether input text contains valid medical symptoms
- **Multi-language Support**: Works with both English and Somali input
- **Smart Suggestions**: Provides helpful suggestions when invalid input is detected
- **Graceful Fallback**: Continues to work even if OpenAI is unavailable

### 2. Disease Prediction Behavior
- **Disease Names**: Always returned in English (never translated)
- **Precautions**: Always returned in Somali (for better user understanding)
- **Input Language**: Preserved for tracking purposes

## Setup

### 1. Environment Variables
Create a `.env` file in the backend directory with:

```env
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=your_mongodb_connection_string
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Test the Integration
```bash
cd backend
python test_openai_validation.py
```

## API Endpoints

### 1. Main Prediction Endpoint
**POST** `/predict`

**Request:**
```json
{
  "symptoms": "I have a headache and fever",
  "lang": "auto",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "message": "Ensemble prediction completed successfully.",
  "type": "diagnosis",
  "disease": "Migraine",  // Always in English
  "confidence": 0.85,
  "precautions": ["La tashii dhakhtar..."],  // Always in Somali
  "lang": "en",
  "validation_result": {
    "is_valid": true,
    "confidence": 0.9,
    "reason": "Contains valid medical symptoms"
  }
}
```

### 2. Symptom Validation Test
**POST** `/test-symptom-validation`

**Request:**
```json
{
  "symptoms": "I have a severe headache",
  "language": "en"
}
```

### 3. Health Check
**GET** `/health`

Returns system status including OpenAI availability.

## Validation Logic

### Valid Symptoms Examples:
- "I have a headache and fever"
- "Waxaan qabaa madax xanuun iyo qandho" (Somali)
- "Experiencing chest pain and difficulty breathing"
- "Nausea, vomiting, and stomach cramps"

### Invalid Input Examples:
- "Hello world, how are you?"
- "I love pizza and movies"
- "The weather is nice today"
- Random text without medical context

## Error Handling

### Invalid Symptoms Response:
```json
{
  "message": "The provided text does not appear to contain valid medical symptoms. Please provide valid medical symptoms such as: headache, fever, pain",
  "type": "invalid_symptoms",
  "validation_result": {
    "is_valid": false,
    "confidence": 0.1,
    "reason": "Text does not contain medical symptoms",
    "suggestions": ["headache", "fever", "pain", "cough"]
  }
}
```

## Testing

### Run the Test Suite:
```bash
python test_openai_validation.py
```

### Manual Testing with curl:
```bash
# Test valid symptoms
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache and fever", "user_id": "test"}'

# Test invalid symptoms
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "Hello world", "user_id": "test"}'

# Test symptom validation directly
curl -X POST http://localhost:5000/test-symptom-validation \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a severe headache", "language": "en"}'
```

## Configuration

### OpenAI Settings:
- **Model**: gpt-3.5-turbo
- **Max Tokens**: 300
- **Temperature**: 0.1 (for consistent responses)
- **Timeout**: Built-in error handling

### Validation Thresholds:
- **Minimum Confidence**: 0.2 (20%)
- **Fallback Behavior**: Accepts input if OpenAI unavailable
- **Suggestion Limit**: 3 suggestions per response

## Troubleshooting

### Common Issues:

1. **OpenAI API Key Missing**
   - Error: "OpenAI not available"
   - Solution: Add OPENAI_API_KEY to .env file

2. **Invalid API Key**
   - Error: "OpenAI validation error"
   - Solution: Check API key validity in OpenAI dashboard

3. **Rate Limiting**
   - Error: "OpenAI validation failed"
   - Solution: Check OpenAI usage limits

4. **Network Issues**
   - Error: "OpenAI validation error"
   - Solution: Check internet connection and firewall settings

## Logging

The application provides detailed logging for debugging:

```
🔍 Validating symptoms with OpenAI: 'I have a headache...'
🤖 OpenAI response: {"is_valid": true, "confidence": 0.9...}
✅ Symptom validation passed (confidence: 0.90)
```

## Performance

- **Validation Time**: ~1-3 seconds per request
- **Fallback Time**: <100ms when OpenAI unavailable
- **Memory Usage**: Minimal (no model loading required)
- **API Calls**: 1 per prediction request

## Security

- API keys are stored in environment variables
- No sensitive data is logged
- Input sanitization is performed
- Rate limiting is handled gracefully
import requests
import json

def test_prediction():
    """Test the prediction endpoint"""
    url = "http://localhost:5000/predict"
    
    # Test data
    test_data = {
        "symptoms": "fever headache cough fatigue",
        "lang": "en",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Prediction test successful!")
        else:
            print("❌ Prediction test failed!")
            
    except Exception as e:
        print(f"❌ Error testing prediction: {str(e)}")

if __name__ == "__main__":
    test_prediction() 
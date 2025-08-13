export const languages = {
  en: {
    // Chat page content
    pageTitle: "AI Health Assistant",
    pageHeading: "Chat with HealthAI",
    pageDescription: "Describe your symptoms in a natural conversation and our AI system will analyze patterns to help predict potential health conditions.",
    aiAssistant: "HealthAI Assistant",
    aiPowered: "AI-powered diagnosis",
    online: "Online",
    
    // Chat interface content
    welcomeMessage: "Hello, I'm HealthAI. Please describe any symptoms you're experiencing, and I'll help predict potential conditions.",
    inputPlaceholder: "Describe your symptoms (e.g., headache, fever, nausea)...",
    disclaimer: "HealthAI is not a replacement for professional medical advice. Always consult a healthcare provider.",
    
    // Prediction responses
    predictionPrefix: "Based on your symptoms, you might be experiencing",
    confidence: "confidence",
    precautions: "Precautions:",
    modelsUsed: "Models used:",
    importantNote: "⚠️ **Important:** This is not a medical diagnosis. Please consult a healthcare professional for proper evaluation and treatment.",
    noPrediction: "I couldn't make a confident prediction based on your symptoms.",
    errorMessage: "I apologize, but I'm having trouble analyzing your symptoms right now.",
    connectionError: "Cannot connect to the prediction service. Please make sure the backend server is running.",
    serviceError: "The prediction service encountered an error. Please try again with different symptoms.",
    invalidInput: "Please provide valid symptom information.",
    
    // Language names
    english: "English",
    somali: "Somali"
  },
  so: {
    // Chat page content
    pageTitle: "Khaladka Caafimaadka AI",
    pageHeading: "La soco HealthAI",
    pageDescription: "Faahfaahin calaamadahaaga si dabiici ah u sharaxaad oo nidaamkeena AI-ga ah ayaa halbeegaya qaabka si uu u sahamiyo xaaladaha caafimaadka.",
    aiAssistant: "Caawiyaha HealthAI",
    aiPowered: "Diagnosis AI-ga ah",
    online: "Online",
    
    // Chat interface content
    welcomeMessage: "Salaam, waxaan ahay HealthAI. Fadlan sharaxaad calaamadaha aad la kulanto, waxaanan kaa caawin doonaa inaan sahamiyo xaaladaha suuragal ah.",
    inputPlaceholder: "Sharaxaad calaamadahaaga (tusaale: madax xanuun, qandho, lafaha)...",
    disclaimer: "HealthAI ma aha mid ku beddelaya talo caafimaad oo professional ah. Mar walba la soco caafimaadka.",
    
    // Prediction responses
    predictionPrefix: "Isku xirnaan calaamadahaaga, waxaad laga yaabaa inaad la kulanto",
    confidence: "kalsoonida",
    precautions: "Taxaddarrada:",
    modelsUsed: "Moodooyinka la adeegsaday:",
    importantNote: "⚠️ **Muhiim:** Tani ma aha diagnosis caafimaad. Fadlan la soco caafimaad professional si aad u helto qiimayn iyo daaweyn sax ah.",
    noPrediction: "Ma awoodin inaan sameeyo sahami kalsooni ah oo ku salaysan calaamadahaaga.",
    errorMessage: "Waan ka xumahay, laakiin waxaan la kulayaa dhibaato inaan halbeegiyo calaamadahaaga hadda.",
    connectionError: "Ma xidhi karin adeegga sahaminta. Fadlan hubi in serverka backend uu socdo.",
    serviceError: "Adeegga sahaminta wuxuu la kulay dhibaato. Fadlan isku day mar kale calaamado kala duwan.",
    invalidInput: "Fadlan bixi macluumaad calaamado ah oo sax ah.",
    
    // Language names
    english: "English",
    somali: "Af-Soomaali"
  }
};

export type Language = keyof typeof languages;

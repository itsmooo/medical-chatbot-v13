DISEASE_RULES = {
    "malaria": {
        "boost_keywords": [
            # Somali symptoms
            "qandho", "dhidid habeenkii", "qaraar", "qaniinyada kaneecada", 
            "taariikhda safarka", "xummad joogto ah", "duuma", "kaneeco",
            # English symptoms
            "fever", "chills", "night sweats", "shaking", "mosquito bite",
            "travel history", "malaria", "sweating", "headache with fever"
        ],
        "penalize_keywords": [
            "sanka duufsan", "qufac", "sanka oo ciriiri ah", "hindhis",
            "runny nose", "nasal congestion", "sneezing", "cold symptoms"
        ],
    },
    "migraine": {
        "boost_keywords": [
            # Somali symptoms
            "madax xanuun", "indho xanuun", "dareen fudud", "dareenka dhawaaqa", 
            "madax xanuun daran", "iftiinka ka cabsi", "qaylada ka cabsi",
            # English symptoms
            "headache", "eye pain", "light sensitivity", "sound sensitivity",
            "migraine", "aura", "visual disturbance", "throbbing pain"
        ],
        "penalize_keywords": [
            "dhidid", "qandho", "shuban", "calool xanuun",
            "fever", "chills", "vomiting", "stomach pain"
        ],
    },
    "typhoid": {
        "boost_keywords": [
            # Somali symptoms
            "xummad raagta", "caloosha xanuunka", "anemia", "matag daran", 
            "jilib xanuun", "shuban", "xaasidka daboolaya",
            # English symptoms
            "prolonged fever", "stomach pain", "headache", "weakness",
            "rose spots", "typhoid", "abdominal pain", "constipation"
        ],
        "penalize_keywords": [
            "sanka duufsan", "qufac gaaban", "hindhis",
            "runny nose", "short cough", "sneezing", "migraine aura"
        ],
    },
    "common cold": {
        "boost_keywords": [
            # Somali symptoms
            "sanka duufsan", "sanka oo ciriiri ah", "qufac", "cuna xanuun", 
            "hindhis", "cuncun cune", "hargab fudud",
            # English symptoms
            "runny nose", "nasal congestion", "cough", "sore throat", 
            "sneezing", "cold", "stuffy nose", "mild fever"
        ],
        "penalize_keywords": [
            "dhidid habeenkii", "caloosha xanuunka", "taariikhda safarka", "qaraar",
            "night chills", "stomach pain", "travel history", "shaking"
        ],
    },
    "pneumonia": {
        "boost_keywords": [
            # Somali symptoms
            "qandho", "qufac", "neefsasho gaaban", "xabad xanuun", 
            "daal", "qufac waxtar leh", "burunkiito",
            # English symptoms
            "fever", "cough", "difficulty breathing", "chest pain", 
            "fatigue", "productive cough", "pneumonia", "shortness of breath"
        ],
        "penalize_keywords": [
            "hindhis", "sanka duufsan", "madax xanuun keliya",
            "sneezing", "runny nose", "headache only", "migraine aura"
        ],
    },
    "diabetes": {
        "boost_keywords": [
            # Somali symptoms
            "sonkor dhiig", "harraad badan", "biyo badan oo la cabo", 
            "miisaan dhimi", "daal joogto ah", "sonkorowga", "kaadi badan",
            # English symptoms
            "blood sugar", "excessive thirst", "frequent urination", 
            "weight loss", "fatigue", "diabetes", "blurred vision", "hunger"
        ],
        "penalize_keywords": [
            "qandho dhakhso ah", "qufac", "sanka duufsan",
            "sudden fever", "cough", "runny nose", "acute symptoms"
        ],
    },
    "urinary tract infection": {
        "boost_keywords": [
            # Somali symptoms
            "kaadi xanuun", "kaadi gubasho", "kaadi joogto ah", 
            "kaadi dhiig leh", "calool hoose xanuun", "infekshanka kaadi",
            # English symptoms
            "painful urination", "burning urination", "frequent urination", 
            "blood in urine", "lower abdominal pain", "uti", "bladder pain"
        ],
        "penalize_keywords": [
            "qufac", "sanka duufsan", "madax xanuun",
            "cough", "runny nose", "headache", "fever alone"
        ],
    },
    "fungal infection": {
        "boost_keywords": [
            # Somali symptoms
            "maqaarka cascas", "qolofka cagaha", "harag cascas", 
            "infekshanka fungal", "qolof burbur", "xuubka cascas",
            # English symptoms
            "itchy skin", "skin rash", "athlete's foot", "fungal infection", 
            "skin peeling", "white patches", "ringworm", "nail infection"
        ],
        "penalize_keywords": [
            "qandho", "qufac", "sanka duufsan", "calool xanuun",
            "fever", "cough", "runny nose", "stomach pain"
        ],
    },
}

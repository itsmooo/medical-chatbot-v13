DISEASE_RULES = {
    "malaria": {
        "boost_keywords": [
            # Somali symptoms
            "qandho", "dhidid habeenkii", "qaraar", "qaniinyada kaneecada", 
            "taariikhda safarka", "xummad joogto ah", "duuma", "kaneeco",
            # English symptoms
            "fever", "chills", "night sweats", "shaking", "mosquito bite",
            "travel history", "malaria", "sweating", "headache with fever",
            "high temperature", "pyrexia", "elevated temperature", "feverish",
            "muscle pain", "joint pain", "body aches", "fatigue", "weakness"
        ],
        "penalize_keywords": [
            "sanka duufsan", "qufac", "sanka oo ciriiri ah", "hindhis",
            "runny nose", "nasal congestion", "sneezing", "cold symptoms",
            "burning urination", "frequent urination", "urinary symptoms"
        ],
    },
    "migraine": {
        "boost_keywords": [
            # Somali symptoms
            "madax xanuun", "indho xanuun", "dareen fudud", "dareenka dhawaaqa", 
            "madax xanuun daran", "iftiinka ka cabsi", "qaylada ka cabsi",
            "madax", "xanuun", "indho", "iftiin", "qaylo", "dareen",
            # English symptoms
            "headache", "eye pain", "light sensitivity", "sound sensitivity",
            "migraine", "aura", "visual disturbance", "throbbing pain",
            "pulsing pain", "severe headache", "one-sided headache",
            "nausea", "vomiting", "dizziness", "blurred vision",
            "photophobia", "phonophobia", "visual aura", "sensory aura",
            "motor aura", "prodrome", "postdrome", "cluster headache",
            "tension headache", "sinus headache", "cervicogenic headache"
        ],
        "penalize_keywords": [
            "dhidid", "qandho", "shuban", "calool xanuun",
            "fever", "chills", "vomiting", "stomach pain",
            "burning urination", "frequent urination", "urinary symptoms",
            "cough", "runny nose", "sore throat", "respiratory symptoms"
        ],
    },
    "typhoid": {
        "boost_keywords": [
            # Somali symptoms
            "xummad raagta", "caloosha xanuunka", "anemia", "matag daran", 
            "jilib xanuun", "shuban", "xaasidka daboolaya",
            # English symptoms
            "prolonged fever", "stomach pain", "headache", "weakness",
            "rose spots", "typhoid", "abdominal pain", "constipation",
            "diarrhea", "loss of appetite", "fatigue", "malaise",
            "step ladder fever", "relative bradycardia", "hepatosplenomegaly"
        ],
        "penalize_keywords": [
            "sanka duufsan", "qufac gaaban", "hindhis",
            "runny nose", "short cough", "sneezing", "migraine aura",
            "burning urination", "frequent urination", "urinary symptoms"
        ],
    },
    "common cold": {
        "boost_keywords": [
            # Somali symptoms
            "sanka duufsan", "sanka oo ciriiri ah", "qufac", "cuna xanuun", 
            "hindhis", "cuncun cune", "hargab fudud",
            # English symptoms
            "runny nose", "nasal congestion", "cough", "sore throat", 
            "sneezing", "cold", "stuffy nose", "mild fever",
            "post-nasal drip", "watery eyes", "mild headache", "fatigue",
            "slight body aches", "scratchy throat", "hoarse voice"
        ],
        "penalize_keywords": [
            "dhidid habeenkii", "caloosha xanuunka", "taariikhda safarka", "qaraar",
            "night chills", "stomach pain", "travel history", "shaking",
            "burning urination", "frequent urination", "urinary symptoms",
            "severe headache", "migraine", "aura", "visual disturbance"
        ],
    },
    "pneumonia": {
        "boost_keywords": [
            # Somali symptoms
            "qandho", "qufac", "neefsasho gaaban", "xabad xanuun", 
            "daal", "qufac waxtar leh", "burunkiito",
            # English symptoms
            "fever", "cough", "difficulty breathing", "chest pain", 
            "fatigue", "productive cough", "pneumonia", "shortness of breath",
            "chest tightness", "rapid breathing", "wheezing", "sweating",
            "chills", "muscle aches", "loss of appetite", "confusion"
        ],
        "penalize_keywords": [
            "hindhis", "sanka duufsan", "madax xanuun keliya",
            "sneezing", "runny nose", "headache only", "migraine aura",
            "burning urination", "frequent urination", "urinary symptoms"
        ],
    },
    "diabetes": {
        "boost_keywords": [
            # Somali symptoms
            "sonkor dhiig", "harraad badan", "biyo badan oo la cabo", 
            "miisaan dhimi", "daal joogto ah", "sonkorowga", "kaadi badan",
            # English symptoms
            "blood sugar", "excessive thirst", "frequent urination", 
            "weight loss", "fatigue", "diabetes", "blurred vision", "hunger",
            "increased appetite", "slow healing", "numbness", "tingling",
            "dry mouth", "dry skin", "recurrent infections"
        ],
        "penalize_keywords": [
            "qandho dhakhso ah", "qufac", "sanka duufsan",
            "sudden fever", "cough", "runny nose", "acute symptoms",
            "chest pain", "difficulty breathing", "severe headache"
        ],
    },
    "urinary tract infection": {
        "boost_keywords": [
            # Somali symptoms
            "kaadi xanuun", "kaadi gubasho", "kaadi joogto ah", 
            "kaadi dhiig leh", "calool hoose xanuun", "infekshanka kaadi",
            # English symptoms
            "painful urination", "burning urination", "frequent urination", 
            "blood in urine", "lower abdominal pain", "uti", "bladder pain",
            "urinary urgency", "urinary frequency", "dysuria", "hematuria",
            "suprapubic pain", "pelvic pain", "cloudy urine", "strong-smelling urine",
            "urinary incontinence", "nocturia", "incomplete bladder emptying"
        ],
        "penalize_keywords": [
            "qufac", "sanka duufsan", "madax xanuun",
            "cough", "runny nose", "headache", "fever alone",
            "chest pain", "difficulty breathing", "severe headache",
            "migraine", "aura", "visual disturbance"
        ],
    },
    "fungal infection": {
        "boost_keywords": [
            # Somali symptoms
            "maqaarka cascas", "qolofka cagaha", "harag cascas", 
            "infekshanka fungal", "qolof burbur", "xuubka cascas",
            # English symptoms
            "itchy skin", "skin rash", "athlete's foot", "fungal infection", 
            "skin peeling", "white patches", "ringworm", "nail infection",
            "jock itch", "yeast infection", "candidiasis", "tinea",
            "scaly skin", "redness", "inflammation", "cracking skin"
        ],
        "penalize_keywords": [
            "qandho", "qufac", "sanka duufsan", "calool xanuun",
            "fever", "cough", "runny nose", "stomach pain",
            "burning urination", "frequent urination", "urinary symptoms",
            "severe headache", "migraine", "chest pain", "difficulty breathing"
        ],
    },
}

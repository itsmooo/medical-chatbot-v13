DISEASE_RULES = {
    "malaria": {
        "boost_keywords": [
            "qandho",
            "dhidid habeenkii",
            "qaraar",
            "qaniinyada kaneecada",
            "taariikhda safarka",
            "xummad joogto ah",
        ],
        "penalize_keywords": ["sanka duufsan", "qufac", "sanka oo ciriiri ah"],
    },
    "migraine": {
        "boost_keywords": [
            "madax xanuun",
            "indho xanuun",
            "dareen fudud",
            "dareenka dhawaaqa",
            "madax xanuun daran",
        ],
        "penalize_keywords": ["dhidid", "qandho", "shuban"],
    },
    "typhoid": {
        "boost_keywords": [
            "xummad raagta",
            "caloosha xanuunka",
            "anemia",
            "matag daran",
            "jilib xanuun",
        ],
        "penalize_keywords": ["aura", "migraine"],
    },
    "common cold": {
        "boost_keywords": [
            "sanka duufsan",
            "sanka oo ciriiri ah",
            "qufac",
            "cuna xanuun",
            "hindhis",
            "cuncun cune",
        ],
        "penalize_keywords": [
            "dhidid habeenkii",
            "caloosha xanuunka",
            "taariikhda safarka",
        ],
    },
    "pneumonia": {
        "boost_keywords": [
            "qandho",
            "qufac",
            "neefsasho gaaban",
            "xabad xanuun",
            "daal",
            "qufac waxtar leh",
        ],
        "penalize_keywords": ["hindhiso", "sanka duufsan", "migraine"],
    },
}

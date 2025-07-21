# disease_rules.py

DISEASE_RULES = {
    "malaria": {
        "boost_keywords": ["qandho", "dhidid habeenkii", "ruxan", "kaneeco", "socdaal", "qandho joogto ah"],
        "penalize_keywords": ["san dareere", "qufac", "sanka xiran"]
    },
    "migraine": {
        "boost_keywords": ["dhanjaf", "il xanuun", "nal neceb", "dhawaq neceb", " madax xanuun daran"],
        "penalize_keywords": ["dhidid", "qandho", "shuban"]
    },
    "typhoid": {
        "boost_keywords": ["qandho muddo dheer ah", "calool xanuun", "dhiig la’aan", "matag badan", "jilbaha xanuun"],
        "penalize_keywords": ["aura", "migraine"]
    },
    "qawowga caadiga ah": {
        "boost_keywords": ["san dareere", "sanka xiran", "qufac", "cunaha xanuun", "hindhiso", "cuncun cunaha"],
        "penalize_keywords": ["dhidid habeenkii", "calool xanuun", "socdaal"]
    }
}

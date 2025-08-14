# 🧹 BACKEND MODEL CLEANUP PLAN

## 📊 Current Situation
- **18+ models** being loaded simultaneously 
- **46 .pkl files** and **9 .h5 files** 
- Multiple duplicate models and legacy versions
- Messy directory structure with multiple versions

## 🎯 Cleanup Strategy

### ✅ KEEP (Best Performing Models)
1. **fixed_v2_ensemble.pkl** (87.68% accuracy) - Primary ensemble
2. **fixed_v2_individual_models.pkl** (87.91% accuracy) - Primary individual models  
3. **One best neural network model** (choose from best_nn_model.h5)
4. **Essential preprocessing files:**
   - fixed_v2/label_encoder.pkl
   - fixed_v2/vectorizer.pkl
   - fixed_v2/feature_scaler.pkl
   - fixed_v2/feature_columns.pkl

### ❌ REMOVE (Redundant/Legacy Models)

#### Legacy & Redundant Models:
- realistic_ranking_model.pkl
- realistic_single_model.pkl  
- ranking_model.pkl
- single_disease_model.pkl
- All individual ML models (random_forest, svm, logistic_regression)

#### Duplicate Neural Networks (Keep only 1):
- deep_neural_network_model.h5
- enhanced_disease_model.h5
- best_model.h5
- fixed_disease_model.h5

#### Old Directories:
- disease_models/v1754895881/
- disease_models_improved/
- disease_figures/ (old figures)
- disease_reports/ (old reports)

### 📁 Final Clean Structure
```
backend/
├── models/
│   ├── ensemble_model.pkl (from fixed_v2)
│   ├── individual_models.pkl (from fixed_v2)
│   ├── neural_network_model.h5 (best performing)
│   ├── label_encoder.pkl
│   ├── vectorizer.pkl
│   ├── feature_scaler.pkl
│   ├── feature_columns.pkl
│   └── precautions_mapping.pkl
├── data/
└── app.py (simplified model loading)
```

## 🚀 Expected Benefits
- **Faster startup time** (load only 3-4 models instead of 18+)
- **Reduced memory usage** (significantly lower RAM consumption)
- **Cleaner codebase** (simplified model loading logic)
- **Better maintainability** (clear model hierarchy)
- **Improved performance** (focus on best models only)

## ⚡ Performance Impact
- Keep only the **top 2 best performing models** (87%+ accuracy)
- Remove **14+ redundant models** 
- **80% reduction** in model files
- **90% reduction** in loading complexity

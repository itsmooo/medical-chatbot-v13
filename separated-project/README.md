# 🧹 SEPARATED PROJECT STRUCTURE

This project has been reorganized into three separate, independent applications:

## 🐍 **Python Flask Backend** (`python-flask-backend/`)
- **Purpose:** Machine Learning disease prediction
- **Technology:** Python + Flask + scikit-learn
- **Contains:** Trained ML models, disease prediction API
- **Port:** 8000
- **Start:** `cd python-flask-backend && python app_clean.py`

## ⚡ **NestJS Backend** (`nestjs-backend/`)  
- **Purpose:** User management, authentication, chat features
- **Technology:** Node.js + NestJS + TypeScript
- **Contains:** Auth, chat, user profiles, database operations
- **Port:** 3001
- **Start:** `cd nestjs-backend && npm run start:dev`

## 🎨 **Next.js Frontend** (`nextjs-frontend/`)
- **Purpose:** User interface and web application
- **Technology:** React + Next.js + TypeScript + Tailwind
- **Contains:** UI components, pages, forms, chat interface
- **Port:** 3000  
- **Start:** `cd nextjs-frontend && npm run dev`

## 🚀 **How to Run All Three:**

### 1. Python Backend (Terminal 1):
```bash
cd python-flask-backend
pip install -r requirements.txt
python app_clean.py
```

### 2. NestJS Backend (Terminal 2):
```bash
cd nestjs-backend
npm install
npm run start:dev
```

### 3. Next.js Frontend (Terminal 3):
```bash
cd nextjs-frontend
npm install
npm run dev
```

## 🎯 **Benefits of Separation:**

✅ **No More Conflicts** - Each project has its own dependencies
✅ **Independent Development** - Work on each part separately  
✅ **Technology Focus** - Python for ML, Node.js for APIs, React for UI
✅ **Easy Deployment** - Deploy each service independently
✅ **Clear Responsibilities** - Each project has a single purpose

## 📡 **API Communication:**

- **Frontend** ↔ **NestJS Backend** (Auth, Chat, Users)
- **Frontend** ↔ **Python Backend** (Disease Predictions)
- **NestJS Backend** ↔ **Python Backend** (ML Integration)

## 🛠️ **Next Steps:**

1. Test each application independently
2. Update API endpoints in frontend to connect to correct backends
3. Configure CORS settings for cross-origin communication
4. Set up environment variables for each project

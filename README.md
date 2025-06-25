# ASMIS - Advanced Sales Management Intelligence System

## 🎯 Overview

ASMIS is a comprehensive sales intelligence platform with MEDDPICC analysis, evidence tracking, and Neural Imprinting Protocol for enhanced decision-making.

## 🏗️ Repository Structure

This is a monorepo containing:

- **`backend/`** - FastAPI-based intelligence engine with MEDDPICC scoring, evidence processing, and stakeholder relationship mapping
- **`frontend-linear/`** - Modern Linear-inspired UI with React 19, Next.js 15, and real-time intelligence features
- **`scripts/`** - Project automation and intelligence system utilities
- **`track_progress/`** - Session tracking and context recovery
- **`.ai/`** - Neural imprinting system with behavioral patterns

## 🚀 Quick Start

### Backend (Intelligence Engine)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend (Linear Intelligence UI)
```bash
cd frontend-linear
npm install --legacy-peer-deps
npm run dev
```

Access the UI at http://localhost:3000/deals

## 📚 Documentation

- **Backend**: `backend/README.md`
- **Frontend**: `frontend-linear/SETUP.md`
- **Intelligence System**: `CLAUDE.md`
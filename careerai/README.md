# 🚀 CareerAI — AI-Based Career Recommendation System

**Author:** Ram Swagath  
**Stack:** React + Vite + Tailwind (Frontend) · FastAPI + MongoDB (Backend) · spaCy + NLP (AI/ML)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Real PDF Scanning | pdfplumber + PyPDF2 extract actual resume text |
| 🎯 ATS Scoring Engine | 8-criteria weighted scoring (0-100) with detailed breakdown |
| 🤖 Career Matching | Cosine similarity across 10 career profiles |
| ⚡ Skill Gap Analysis | Identifies missing high-value skills |
| 🗺️ Learning Roadmap | Personalized 5-stage career progression path |
| 📊 Analytics Dashboard | Market trends, salary data, demand forecasting |
| 🎓 Course Recommendations | Coursera, Udemy, edX suggestions mapped to gaps |
| 💬 AI Career Chatbot | Context-aware career assistant |
| 🔐 JWT Authentication | Secure register/login with refresh tokens |
| 👑 Admin Panel | User management and dataset analytics |
| 🐳 Docker Support | One-command deployment |
| 🚢 CI/CD Ready | GitHub Actions → Render + Vercel |

---

## 📁 Project Structure

```
careerai/
├── backend/
│   ├── main.py                     # FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── app/
│       ├── api/
│       │   ├── auth.py             # JWT auth routes
│       │   ├── resume.py           # Upload + analysis routes
│       │   ├── careers.py          # Career listing + recommendations
│       │   ├── analytics.py        # Dashboard analytics
│       │   ├── chatbot.py          # AI chat assistant
│       │   ├── courses.py          # Course recommendations
│       │   └── admin.py            # Admin panel routes
│       ├── core/
│       │   ├── config.py           # Pydantic settings
│       │   ├── database.py         # Motor async MongoDB
│       │   └── security.py        # JWT + bcrypt
│       ├── ml/
│       │   ├── ats_scorer.py       # 8-criteria ATS scoring engine
│       │   ├── career_recommender.py # Cosine similarity matching
│       │   └── text_extractor.py  # PDF/DOCX/TXT text extraction
│       ├── models/
│       │   ├── user.py             # User schemas
│       │   └── resume.py           # Resume schemas
│       └── middleware/
│           ├── logging.py          # Request logging
│           └── rate_limit.py      # IP-based rate limiting
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── services/api.js         # Axios API client with interceptors
│       └── store/
│           ├── authStore.js        # Zustand auth state
│           └── resumeStore.js     # Zustand resume state
├── docker-compose.yml
└── .github/workflows/ci.yml
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- MongoDB (local or Atlas)
- Docker (optional)

### Option A — Docker (Recommended)

```bash
git clone https://github.com/yourusername/careerai.git
cd careerai
cp backend/.env.example backend/.env
# Edit backend/.env with your secrets
docker-compose up --build
```

- Frontend: http://localhost:5173  
- Backend API: http://localhost:8000  
- API Docs: http://localhost:8000/api/docs

---

### Option B — Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

cp .env.example .env
# Edit .env — set MONGODB_URL and JWT_SECRET_KEY

uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000/api" > .env
npm run dev
```

---

## 🌐 Deployment

### Backend → Render

1. Push to GitHub
2. Create new **Web Service** on [render.com](https://render.com)
3. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`

### Frontend → Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
# Set VITE_API_URL to your Render backend URL
```

### Database → MongoDB Atlas

1. Create free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Whitelist all IPs (0.0.0.0/0) for Render
3. Copy connection string to `MONGODB_URL` in Render env vars

---

## 🔌 API Reference

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, get JWT tokens |
| GET | `/api/auth/me` | Get current user profile |
| POST | `/api/auth/refresh` | Refresh access token |

### Resume
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/resume/upload` | Upload + analyze resume (PDF/DOCX/TXT) |
| GET | `/api/resume/history` | Get user's resume history |
| GET | `/api/resume/{id}` | Get specific resume analysis |
| DELETE | `/api/resume/{id}` | Delete resume |

### Careers & Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/careers/` | List all career profiles |
| GET | `/api/careers/recommend?skills=X` | Get recommendations |
| GET | `/api/analytics/dashboard` | Dashboard stats + trends |
| GET | `/api/courses/` | List courses (optional: ?skill=Python) |
| POST | `/api/chatbot/message` | Send chat message |

---

## 🎯 ATS Scoring Breakdown

| Criterion | Weight | What's Measured |
|---|---|---|
| Keyword Density | 22% | Tech skills vs. industry vocabulary |
| Work Experience | 22% | Action verbs, bullet points, quantified results |
| Contact Info | 12% | Email, phone, LinkedIn, GitHub |
| Education | 12% | Degree level detection |
| Skills Section | 10% | Dedicated skills header + count |
| Format & Structure | 8% | Section headers, word count, readability |
| Certifications | 7% | Industry certs (AWS, CompTIA, etc.) |
| Achievements | 7% | Quantified metrics (%, $, numbers) |

---

## 🛡️ Environment Variables

```env
# Required
JWT_SECRET_KEY=your-256-bit-secret
MONGODB_URL=mongodb+srv://...

# Optional
DEBUG=false
MAX_FILE_SIZE_MB=10
ALLOWED_ORIGINS=["https://careerai.vercel.app"]
```

---

## 📜 License

MIT License — Ram Swagath © 2025

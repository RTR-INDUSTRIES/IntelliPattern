# 🚀 Deployment Guide - Academic Pattern Detector

## Overview
This guide helps you deploy your Academic Pattern Detector with user authentication and database storage to Vercel.

## 📋 Prerequisites

### 1. Free Database Setup (Choose One)

#### Option A: Neon (Recommended)
1. Go to [neon.tech](https://neon.tech)
2. Sign up for free account
3. Create a new project
4. Copy your connection string (looks like: `postgresql://user:password@host/database`)

#### Option B: Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → Database
4. Copy connection string

#### Option C: Railway
1. Go to [railway.app](https://railway.app)
2. Create new project → Add PostgreSQL
3. Copy connection string from variables

### 2. API Keys
- **Gemini AI**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Flask Secret**: Generate a secure random key (32+ characters)

## 🔧 Local Development Setup

### 1. Install Dependencies
```bash
pip install -r requirements_updated.txt
```

### 2. Environment Variables
Create `.env` file:
```bash
# Database (from Neon, Supabase, or Railway)
DATABASE_URL=postgresql://username:password@host:5432/database_name

# Flask Configuration
FLASK_SECRET_KEY=your_super_secret_key_here_min_32_chars
FLASK_ENV=development

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Database Initialization
```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Run Locally
```bash
python app.py
```

## 🌐 Vercel Deployment

### 1. GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/academic-pattern-detector.git
git push -u origin main
```

### 2. Vercel Setup
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure Environment Variables:

**Required Environment Variables:**
```
DATABASE_URL=postgresql://your_database_connection_string
FLASK_SECRET_KEY=your_super_secret_key_32_chars_minimum
GEMINI_API_KEY=your_gemini_api_key
FLASK_ENV=production
```

### 3. Deploy
- Vercel will automatically deploy
- Your app will be available at `your-app-name.vercel.app`

## 📊 Database Management

### Tables Created:
- `users` - User authentication
- `study_sessions` - User study data
- `performance_records` - Academic performance
- `wellness_tracking` - Wellness metrics

### Features:
- **User Authentication**: Login/logout with email & password
- **Data Isolation**: Each user's data is separate
- **Persistent Storage**: All data saved to PostgreSQL
- **AI Insights**: Personalized to each user's data

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ Session management with Flask-Login
- ✅ CSRF protection with Flask-WTF
- ✅ SQL injection prevention with SQLAlchemy
- ✅ Environment variable protection

## 📱 Features Added

### User System:
- Email/password registration
- Secure login/logout
- Remember me functionality
- Password validation

### Database Integration:
- PostgreSQL for production
- User data isolation
- Persistent AI insights
- Performance tracking

## 🛠️ File Structure
```
├── app.py              # Main Flask application (updated)
├── models.py           # Database models
├── forms.py            # Authentication forms
├── vercel.json         # Vercel deployment config
├── requirements_updated.txt  # Updated dependencies
├── .env.production     # Environment template
├── templates/
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   └── ...            # Existing templates
└── DEPLOYMENT.md       # This guide
```

## ⚡ Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements_updated.txt

# 2. Set up environment variables (copy .env.production to .env)

# 3. Initialize database (after setting DATABASE_URL)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 4. Run locally
python app.py

# 5. Deploy to Vercel
git add . && git commit -m "Deploy" && git push
```

## 🎯 Next Steps

1. **Set up your database** (Neon recommended)
2. **Get Gemini API key**
3. **Update requirements.txt** to `requirements_updated.txt`
4. **Update app.py** with authentication code
5. **Deploy to Vercel**

## 💡 Cost Breakdown (All Free Tiers)

- **Neon PostgreSQL**: 512MB storage, 1 database
- **Vercel Hosting**: 100GB bandwidth, serverless functions
- **Google Gemini**: Generous free tier
- **Total Monthly Cost**: $0 🎉

## 🔧 Troubleshooting

### Common Issues:
1. **Database Connection**: Ensure DATABASE_URL is correct
2. **Environment Variables**: Check all required vars are set in Vercel
3. **Migration Errors**: Run `flask db upgrade` after deployment
4. **Import Errors**: Ensure all dependencies in requirements.txt

Need help? The app includes error handling and detailed logs! 🚀

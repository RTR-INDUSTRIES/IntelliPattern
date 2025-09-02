# IntelliPattern - Academic Performance Pattern Detector

A comprehensive web application that helps students optimize their learning by tracking study habits, analyzing wellness patterns, and providing AI-powered insights for academic success.

## Project Overview

IntelliPattern is an intelligent academic performance tracking system that combines data analytics with artificial intelligence to help students understand their learning patterns and improve their academic outcomes. The application tracks study sessions, academic performance, and wellness metrics to provide personalized recommendations through Google Gemini AI integration.

## Features

### Core Functionality
- **Study Session Tracking**: Log study sessions with duration, subjects, methods, and focus ratings
- **Performance Recording**: Track test scores, assignments, and academic assessments
- **Wellness Monitoring**: Record sleep patterns, stress levels, mood, and physical activity
- **AI-Powered Insights**: Get personalized recommendations using Google Gemini AI
- **Pattern Analysis**: Discover correlations between study habits and academic performance
- **Data Visualization**: Interactive charts and statistics dashboard

### User Management
- **Secure Authentication**: Email-based registration and login system
- **Password Security**: bcrypt hashing for secure password storage
- **Session Management**: Persistent login sessions with Flask-Login
- **Account Management**: Users can securely delete their accounts
- **Data Privacy**: Complete user data isolation and privacy

## Technology Stack

### Backend
- **Framework**: Flask (Python web framework)
- **Database**: PostgreSQL (Neon.tech for production)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login with bcrypt password hashing
- **Forms**: Flask-WTF with WTForms validation
- **Database Migrations**: Flask-Migrate

### Frontend
- **Styling**: Tailwind CSS for responsive design
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome
- **Animations**: AOS (Animate On Scroll)

### AI Integration
- **AI Service**: Google Gemini AI (gemini-1.5-flash-latest)
- **API**: google-generativeai Python library

### Deployment
- **Hosting**: Vercel serverless platform
- **Database**: Neon.tech PostgreSQL cloud database
- **Version Control**: Git with GitHub

## Database Schema

### Users Table
- User authentication and profile information
- Password hashing with bcrypt
- Account creation and login timestamps

### Study Sessions Table
- Subject, duration, study methods
- Focus ratings and difficulty levels
- Start/end times and session notes

### Performance Records Table
- Academic assessments and scores
- Subject-wise performance tracking
- Assessment types and topics covered

### Wellness Tracking Table
- Sleep hours and quality metrics
- Stress levels and mood ratings
- Exercise minutes and caffeine intake

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (or use Neon.tech)
- Google Gemini AI API key

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/RTR-INDUSTRIES/IntelliPattern.git
cd IntelliPattern
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
Create a `.env` file:
```
DATABASE_URL=your_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_32_character_secret_key
FLASK_ENV=development
```

4. **Database Setup**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run the application**
```bash
python app.py
```

## Deployment

### Vercel Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy to Vercel**
- Connect your GitHub repository to Vercel
- Configure environment variables in Vercel dashboard
- Automatic deployment on push

### Required Environment Variables
```
DATABASE_URL=postgresql://username:password@host:port/database
GEMINI_API_KEY=your_google_gemini_api_key
FLASK_SECRET_KEY=secure_random_32_character_string
FLASK_ENV=production
```

## Project Structure

```
IntelliPattern/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── forms.py              # WTForms for user input
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment configuration
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   └── ...
├── static/              # Static assets
└── Screenshots/         # Application screenshots
```

## Key Components

### Authentication System
- Secure user registration and login
- Password validation and hashing
- Session management and logout functionality
- Account deletion with data cleanup

### Data Analytics
- Study pattern recognition
- Performance correlation analysis
- Wellness impact assessment
- Trend identification over time

### AI Integration
- Personalized study recommendations
- Performance optimization suggestions
- Wellness and productivity correlations
- Learning efficiency insights

## Security Features

- **Password Security**: bcrypt hashing with salt
- **CSRF Protection**: Flask-WTF form validation
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Session Security**: Flask-Login secure sessions
- **Input Validation**: Server-side form validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Author

**Abhinaba Paul**  
Computer Science Student at VIT, Vellore

## Support

For issues, questions, or contributions, please open an issue on GitHub or contact the development team.

---

Built with modern web technologies and AI integration to help students achieve academic excellence through data-driven insights.

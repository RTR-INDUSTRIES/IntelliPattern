from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Load Flask SECRET_KEY from environment for security
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev')  # fallback to 'dev' for local dev

# Configure Gemini AI (Google Generative AI)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    # The latest google-generativeai just needs the API key set before using GenerativeModel
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("✅ Gemini AI configured successfully!")
else:
    model = None
    print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")

# Database setup
DATABASE = 'instance/database.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    conn = get_db_connection()
    
    # Create study_sessions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            duration INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            study_method TEXT NOT NULL,
            difficulty_level INTEGER NOT NULL,
            focus_rating INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create performance_records table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS performance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            date TEXT NOT NULL,
            topics_covered TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create wellness_tracking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS wellness_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            sleep_hours REAL NOT NULL,
            stress_level INTEGER NOT NULL,
            mood_rating INTEGER NOT NULL,
            exercise_minutes INTEGER DEFAULT 0,
            caffeine_intake INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_ai_insights():
    """Get AI insights from user's study data"""
    if not model:
        return "🤖 AI analysis unavailable - Please configure your API key in the .env file."
    
    try:
        conn = get_db_connection()
        
        # Get comprehensive data
        study_data = conn.execute('''
            SELECT subject, duration, focus_rating, difficulty_level, 
                   study_method, DATE(created_at) as date,
                   TIME(start_time) as start_time, TIME(end_time) as end_time
            FROM study_sessions 
            ORDER BY created_at DESC LIMIT 20
        ''').fetchall()
        
        performance_data = conn.execute('''
            SELECT subject, score, max_score, assessment_type, date
            FROM performance_records
            ORDER BY date DESC LIMIT 10
        ''').fetchall()
        
        wellness_data = conn.execute('''
            SELECT sleep_hours, stress_level, mood_rating, 
                   exercise_minutes, caffeine_intake, DATE(date) as date
            FROM wellness_tracking
            ORDER BY date DESC LIMIT 10
        ''').fetchall()
        
        # Get summary statistics
        stats = conn.execute('''
            SELECT 
                COUNT(*) as total_sessions,
                AVG(focus_rating) as avg_focus,
                AVG(duration) as avg_duration,
                COUNT(DISTINCT subject) as subjects_count
            FROM study_sessions
        ''').fetchone()
        
        conn.close()
        
        # Check if there's enough data for meaningful analysis
        if len(study_data) < 3:
            return """🚀 **Getting Started with AI Analysis**

Welcome to your AI Learning Coach! I'm here to help you optimize your academic performance.

**Current Status:** You have {} study session(s) logged. To provide meaningful insights, I recommend logging at least 5-10 study sessions along with some wellness data.

**Quick Tips to Get Started:**
• Log your study sessions with honest focus ratings
• Track your sleep and stress levels in the wellness section
• Record any test scores or assignment grades
• Be consistent - even 5 minutes of logging can reveal patterns!

**What I'll Analyze Once You Have More Data:**
✨ Peak performance times and optimal study durations
📊 Correlations between sleep, stress, and focus
📚 Which subjects and study methods work best for you
🎯 Personalized recommendations for improvement

Keep logging your data - I'll be ready with insights soon! 🎓""".format(len(study_data))
        
        # Prepare data for AI analysis
        data_summary = {
            "stats": dict(stats) if stats else {},
            "study_sessions": [dict(row) for row in study_data],
            "performance_records": [dict(row) for row in performance_data],
            "wellness_data": [dict(row) for row in wellness_data]
        }
        
        # Create AI prompt
        prompt = f"""
        You are an expert AI learning coach analyzing a student's academic performance data. Be encouraging, specific, and actionable.

        Student Data Analysis:
        {json.dumps(data_summary, indent=2)}

        Provide insights in this format:

        **🎯 KEY PATTERNS DISCOVERED**
        [Identify 2-3 most important patterns in their data]

        **📊 PERFORMANCE CORRELATIONS** 
        [Correlations between wellness factors and academic performance]

        **💪 YOUR STRENGTHS**
        [What they're doing well - be specific with data]

        **🚀 OPTIMIZATION OPPORTUNITIES**
        [Specific, actionable recommendations]

        **📅 NEXT STEPS**
        [Concrete actions they can take this week]

        Keep response under 400 words. Use data points and be encouraging. Include emojis for engagement.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"AI Analysis Error: {str(e)}")
        return f"""🤖 **AI Analysis Temporarily Unavailable**

I'm having trouble analyzing your data right now, but don't worry! Here are some general insights while I get back online:

**Keep These Habits Strong:**
• Maintain consistent study sessions
• Track your focus and energy levels honestly  
• Log your wellness data regularly

**Try This Week:**
• Experiment with different study times to find your peak hours
• Notice how sleep affects your focus ratings
• Test different study methods and see what works

Error details: {str(e)}

Try refreshing the page in a few minutes! 🔄"""

@app.route('/')
def home():
    return render_template('base.html', 
                         title='Academic Performance Pattern Detector',
                         message='Welcome to Your Personal Learning Coach!')

@app.route('/dashboard')
def dashboard():
    # Get recent study sessions for dashboard
    conn = get_db_connection()
    recent_sessions = conn.execute(
        'SELECT * FROM study_sessions ORDER BY created_at DESC LIMIT 5'
    ).fetchall()
    
    # Get basic statistics
    total_sessions = conn.execute('SELECT COUNT(*) as count FROM study_sessions').fetchone()['count']
    total_hours = conn.execute('SELECT SUM(duration) as total FROM study_sessions').fetchone()['total'] or 0
    avg_focus = conn.execute('SELECT AVG(focus_rating) as avg FROM study_sessions').fetchone()['avg'] or 0
    
    conn.close()
    
    return render_template('dashboard.html', 
                         title='Dashboard',
                         recent_sessions=recent_sessions,
                         total_sessions=total_sessions,
                         total_hours=round(total_hours/60, 1),  # Convert minutes to hours
                         avg_focus=round(avg_focus, 1))

@app.route('/log-study', methods=['GET', 'POST'])
def log_study():
    if request.method == 'POST':
        # Get form data
        subject = request.form['subject']
        duration = int(request.form['duration'])
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        study_method = request.form['study_method']
        difficulty_level = int(request.form['difficulty_level'])
        focus_rating = int(request.form['focus_rating'])
        notes = request.form.get('notes', '')
        
        # Insert into database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO study_sessions 
            (subject, duration, start_time, end_time, study_method, difficulty_level, focus_rating, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (subject, duration, start_time, end_time, study_method, difficulty_level, focus_rating, notes))
        conn.commit()
        conn.close()
        
        flash('Study session logged successfully! 📚', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('log_study.html', title='Log Study Session')

@app.route('/patterns')
def patterns():
    """Analyze patterns in study data"""
    conn = get_db_connection()
    
    # Get correlation between focus rating and study duration
    focus_data = conn.execute('''
        SELECT focus_rating, AVG(duration) as avg_duration 
        FROM study_sessions 
        GROUP BY focus_rating
        ORDER BY focus_rating
    ''').fetchall()
    
    # Get best performing subjects
    subject_performance = conn.execute('''
        SELECT s.subject, AVG(s.focus_rating) as avg_focus, 
               COUNT(s.id) as session_count,
               SUM(s.duration) as total_minutes
        FROM study_sessions s
        GROUP BY s.subject
        HAVING session_count >= 2
        ORDER BY avg_focus DESC
    ''').fetchall()
    
    # Get wellness correlation (if data exists)
    wellness_study_correlation = conn.execute('''
        SELECT w.sleep_hours, w.stress_level, AVG(s.focus_rating) as avg_focus
        FROM wellness_tracking w
        JOIN study_sessions s ON DATE(w.date) = DATE(s.created_at)
        GROUP BY w.sleep_hours, w.stress_level
        HAVING COUNT(*) >= 2
    ''').fetchall()
    
    conn.close()
    
    patterns = []
    
    # Analyze focus patterns
    if focus_data:
        high_focus_sessions = [row for row in focus_data if row['focus_rating'] >= 4]
        if high_focus_sessions:
            avg_duration = sum(row['avg_duration'] for row in high_focus_sessions) / len(high_focus_sessions)
            patterns.append({
                'title': '🎯 High Focus Sessions',
                'description': f'Your high-focus sessions (4-5 rating) average {avg_duration:.0f} minutes',
                'recommendation': 'Try to replicate conditions that lead to high focus sessions!',
                'type': 'positive'
            })
    
    # Analyze subject performance
    if subject_performance:
        best_subject = subject_performance[0]
        patterns.append({
            'title': f'📚 Top Subject: {best_subject["subject"]}',
            'description': f'Average focus rating: {best_subject["avg_focus"]:.1f}/5 ({best_subject["session_count"]} sessions)',
            'recommendation': f'You focus well on {best_subject["subject"]}. Apply similar techniques to other subjects.',
            'type': 'insight'
        })
        
        # Check for struggling subjects
        if len(subject_performance) > 1:
            struggling_subject = subject_performance[-1]
            if struggling_subject['avg_focus'] < 3.0:
                patterns.append({
                    'title': f'⚠️ Needs Attention: {struggling_subject["subject"]}',
                    'description': f'Average focus rating: {struggling_subject["avg_focus"]:.1f}/5',
                    'recommendation': f'Try different study methods for {struggling_subject["subject"]} or study it when you\'re most alert.',
                    'type': 'warning'
                })
    
    # Analyze wellness correlation
    if wellness_study_correlation:
        high_sleep_focus = [row for row in wellness_study_correlation if row['sleep_hours'] >= 7]
        if high_sleep_focus:
            avg_focus_good_sleep = sum(row['avg_focus'] for row in high_sleep_focus) / len(high_sleep_focus)
            patterns.append({
                'title': '😴 Sleep & Focus Connection',
                'description': f'With 7+ hours sleep, your average focus is {avg_focus_good_sleep:.1f}/5',
                'recommendation': 'Prioritize getting enough sleep for better study sessions!',
                'type': 'insight'
            })
    
    # If no patterns found
    if not patterns:
        patterns.append({
            'title': '📊 Getting Started',
            'description': 'Keep logging your study sessions to discover your personal learning patterns!',
            'recommendation': 'Try logging at least 5-10 study sessions to see meaningful insights.',
            'type': 'info'
        })
    
    return render_template('patterns.html', title='Pattern Analysis', patterns=patterns)

@app.route('/ai-insights')
def ai_insights():
    """Display AI-powered insights"""
    print("🤖 Generating AI insights...")
    insight = get_ai_insights()
    
    # Get data point count for display
    conn = get_db_connection()
    data_points = (
        conn.execute('SELECT COUNT(*) as count FROM study_sessions').fetchone()['count'] +
        conn.execute('SELECT COUNT(*) as count FROM performance_records').fetchone()['count'] +
        conn.execute('SELECT COUNT(*) as count FROM wellness_tracking').fetchone()['count']
    )
    conn.close()
    
    return render_template('ai_insights.html', 
                         title='AI Insights',
                         insight=insight,
                         data_points=data_points)

@app.route('/log-performance', methods=['GET', 'POST'])
def log_performance():
    if request.method == 'POST':
        subject = request.form['subject']
        assessment_type = request.form['assessment_type']
        score = float(request.form['score'])
        max_score = float(request.form['max_score'])
        date = request.form['date']
        topics_covered = request.form.get('topics_covered', '')
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO performance_records 
            (subject, assessment_type, score, max_score, date, topics_covered)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (subject, assessment_type, score, max_score, date, topics_covered))
        conn.commit()
        conn.close()
        
        flash('Performance record added successfully! 📈', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('log_performance.html', title='Log Performance')

@app.route('/log-wellness', methods=['GET', 'POST'])
def log_wellness():
    if request.method == 'POST':
        date = request.form['date']
        sleep_hours = float(request.form['sleep_hours'])
        stress_level = int(request.form['stress_level'])
        mood_rating = int(request.form['mood_rating'])
        exercise_minutes = int(request.form.get('exercise_minutes', 0))
        caffeine_intake = int(request.form.get('caffeine_intake', 0))
        notes = request.form.get('notes', '')
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO wellness_tracking 
            (date, sleep_hours, stress_level, mood_rating, exercise_minutes, caffeine_intake, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, sleep_hours, stress_level, mood_rating, exercise_minutes, caffeine_intake, notes))
        conn.commit()
        conn.close()
        
        flash('Wellness data logged successfully! 💪', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('log_wellness.html', title='Log Wellness')

@app.route('/api/study-data')
def api_study_data():
    """API endpoint to get study data for charts"""
    conn = get_db_connection()
    
    # Get study hours by subject
    subject_data = conn.execute('''
        SELECT subject, SUM(duration) as total_minutes 
        FROM study_sessions 
        GROUP BY subject
    ''').fetchall()
    
    # Get daily study hours for last 7 days
    daily_data = conn.execute('''
        SELECT DATE(created_at) as date, SUM(duration) as total_minutes
        FROM study_sessions 
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY date
    ''').fetchall()
    
    conn.close()
    
    return jsonify({
        'subjects': [{'subject': row['subject'], 'hours': round(row['total_minutes']/60, 1)} for row in subject_data],
        'daily': [{'date': row['date'], 'hours': round(row['total_minutes']/60, 1)} for row in daily_data]
    })

@app.route('/delete-study-session/<int:session_id>', methods=['POST'])
def delete_study_session(session_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM study_sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()
    flash('Study session deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete-performance-record/<int:record_id>', methods=['POST'])
def delete_performance_record(record_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM performance_records WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
    flash('Performance record deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete-wellness-entry/<int:entry_id>', methods=['POST'])
def delete_wellness_entry(entry_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wellness_tracking WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    flash('Wellness entry deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()  # Initialize database when app starts
    app.run(debug=True)
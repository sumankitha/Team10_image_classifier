"""
Admin Dashboard for Team10 Image Classifier
Handles FAQ management, PDF/CSV ingestion, and analytics
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json
import pandas as pd
import PyPDF2
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'team10-admin-dashboard-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Database Models
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class ConversationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_question = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_feedback = db.Column(db.String(20))  # positive, negative, neutral
    session_id = db.Column(db.String(100))

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # pdf, csv
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    content_preview = db.Column(db.Text)

# Routes
@app.route('/')
def dashboard():
    """Main dashboard with overview statistics"""
    faq_count = FAQ.query.filter_by(is_active=True).count()
    total_conversations = ConversationLog.query.count()
    recent_uploads = UploadedFile.query.order_by(UploadedFile.upload_date.desc()).limit(5).all()
    recent_conversations = ConversationLog.query.order_by(ConversationLog.timestamp.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         faq_count=faq_count,
                         total_conversations=total_conversations,
                         recent_uploads=recent_uploads,
                         recent_conversations=recent_conversations)

@app.route('/faqs')
def list_faqs():
    """List all FAQs with search and filter options"""
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = FAQ.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(FAQ.question.contains(search) | FAQ.answer.contains(search))
    
    faqs = query.order_by(FAQ.updated_at.desc()).all()
    categories = db.session.query(FAQ.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('faqs.html', faqs=faqs, categories=categories, 
                         current_category=category, search=search)

@app.route('/faqs/add', methods=['GET', 'POST'])
def add_faq():
    """Add a new FAQ"""
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category = request.form['category']
        
        if question and answer:
            faq = FAQ(question=question, answer=answer, category=category)
            db.session.add(faq)
            db.session.commit()
            flash('FAQ added successfully!', 'success')
            return redirect(url_for('list_faqs'))
        else:
            flash('Please fill in all required fields.', 'error')
    
    return render_template('add_faq.html')

@app.route('/faqs/edit/<int:faq_id>', methods=['GET', 'POST'])
def edit_faq(faq_id):
    """Edit an existing FAQ"""
    faq = FAQ.query.get_or_404(faq_id)
    
    if request.method == 'POST':
        faq.question = request.form['question']
        faq.answer = request.form['answer']
        faq.category = request.form['category']
        faq.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('FAQ updated successfully!', 'success')
        return redirect(url_for('list_faqs'))
    
    return render_template('edit_faq.html', faq=faq)

@app.route('/faqs/delete/<int:faq_id>', methods=['POST'])
def delete_faq(faq_id):
    """Soft delete an FAQ"""
    faq = FAQ.query.get_or_404(faq_id)
    faq.is_active = False
    db.session.commit()
    flash('FAQ deleted successfully!', 'success')
    return redirect(url_for('list_faqs'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads (PDF/CSV)"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file and extract preview
            file_type = filename.rsplit('.', 1)[1].lower()
            content_preview = process_uploaded_file(file_path, file_type)
            
            # Save file record to database
            uploaded_file = UploadedFile(
                filename=filename,
                file_type=file_type,
                content_preview=content_preview,
                processed=True
            )
            db.session.add(uploaded_file)
            db.session.commit()
            
            flash(f'File {filename} uploaded and processed successfully!', 'success')
            return redirect(url_for('list_uploads'))
        else:
            flash('Invalid file type. Only PDF and CSV files are allowed.', 'error')
    
    return render_template('upload.html')

@app.route('/uploads')
def list_uploads():
    """List all uploaded files"""
    uploads = UploadedFile.query.order_by(UploadedFile.upload_date.desc()).all()
    return render_template('uploads.html', uploads=uploads)

@app.route('/analytics')
def analytics():
    """Show analytics and conversation statistics"""
    # Get conversation statistics
    total_conversations = ConversationLog.query.count()
    
    # Get feedback statistics
    positive_feedback = ConversationLog.query.filter_by(user_feedback='positive').count()
    negative_feedback = ConversationLog.query.filter_by(user_feedback='negative').count()
    neutral_feedback = ConversationLog.query.filter_by(user_feedback='neutral').count()
    
    # Get daily conversation counts for the last 7 days
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    daily_stats = []
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        count = ConversationLog.query.filter(
            db.func.date(ConversationLog.timestamp) == date
        ).count()
        daily_stats.append({'date': date.strftime('%Y-%m-%d'), 'count': count})
    
    # Get top FAQ categories
    category_stats = db.session.query(
        FAQ.category,
        db.func.count(FAQ.id).label('count')
    ).filter_by(is_active=True).group_by(FAQ.category).all()
    
    return render_template('analytics.html',
                         total_conversations=total_conversations,
                         positive_feedback=positive_feedback,
                         negative_feedback=negative_feedback,
                         neutral_feedback=neutral_feedback,
                         daily_stats=daily_stats,
                         category_stats=category_stats)

@app.route('/logs')
def conversation_logs():
    """View conversation logs"""
    page = request.args.get('page', 1, type=int)
    logs = ConversationLog.query.order_by(ConversationLog.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('logs.html', logs=logs)

# API endpoints for external integrations
@app.route('/api/faq/<int:faq_id>')
def api_get_faq(faq_id):
    """API endpoint to get a specific FAQ"""
    faq = FAQ.query.get_or_404(faq_id)
    return jsonify({
        'id': faq.id,
        'question': faq.question,
        'answer': faq.answer,
        'category': faq.category
    })

@app.route('/api/faqs')
def api_list_faqs():
    """API endpoint to list all active FAQs"""
    faqs = FAQ.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': faq.id,
        'question': faq.question,
        'answer': faq.answer,
        'category': faq.category
    } for faq in faqs])

@app.route('/api/log_conversation', methods=['POST'])
def api_log_conversation():
    """API endpoint to log a conversation"""
    data = request.get_json()
    
    log = ConversationLog(
        user_question=data.get('question', ''),
        bot_response=data.get('response', ''),
        user_feedback=data.get('feedback'),
        session_id=data.get('session_id')
    )
    
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Conversation logged'})

# Helper functions
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'csv'}

def process_uploaded_file(file_path, file_type):
    """Process uploaded file and return content preview"""
    try:
        if file_type == 'pdf':
            return extract_pdf_preview(file_path)
        elif file_type == 'csv':
            return extract_csv_preview(file_path)
    except Exception as e:
        return f"Error processing file: {str(e)}"
    
    return "File processed successfully"

def extract_pdf_preview(file_path):
    """Extract first few lines from PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            if len(pdf_reader.pages) > 0:
                first_page = pdf_reader.pages[0]
                text = first_page.extract_text()
                # Return first 500 characters
                return text[:500] + "..." if len(text) > 500 else text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    
    return "PDF file uploaded"

def extract_csv_preview(file_path):
    """Extract preview from CSV file"""
    try:
        df = pd.read_csv(file_path)
        preview = f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
        preview += f"Columns: {', '.join(df.columns.tolist())}\n"
        preview += "First 3 rows:\n"
        preview += df.head(3).to_string()
        return preview
    except Exception as e:
        return f"Error reading CSV: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
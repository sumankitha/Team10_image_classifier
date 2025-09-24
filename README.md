# Team10 Image Classifier - Admin Dashboard

A comprehensive admin panel for managing FAQs, handling file uploads, and monitoring system analytics for the Team10 Image Classifier project.

## Features

### 🎯 Core Functionality
- **FAQ Management**: Create, edit, delete, and organize frequently asked questions
- **File Upload System**: Support for PDF and CSV file ingestion with automatic processing
- **Analytics Dashboard**: Real-time statistics and performance metrics
- **Conversation Logging**: Track user interactions and feedback
- **Data Export**: Export conversation logs in CSV or JSON format

### 🛠️ Technical Features
- **RESTful API**: Full API support for external integrations
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **File Processing**: Automatic text extraction from PDFs and CSV analysis
- **Real-time Updates**: Live statistics and data visualization

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sumankitha/Team10_image_classifier.git
   cd Team10_image_classifier
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### FAQ Management
- `GET /api/faqs` - List all active FAQs
- `GET /api/faq/<id>` - Get specific FAQ by ID

### Conversation Logging
- `POST /api/log_conversation` - Log a conversation
  ```json
  {
    "question": "User question",
    "response": "Bot response", 
    "feedback": "positive|negative|neutral",
    "session_id": "unique_session_id"
  }
  ```

## Usage Examples

### Adding FAQs
1. Navigate to the FAQs section
2. Click "Add New FAQ"
3. Fill in the question, answer, and category
4. Save the FAQ

### Uploading Files
1. Go to the Upload Files section
2. Select a PDF or CSV file (max 16MB)
3. The system will automatically process and extract content
4. View processed files in the Files section

### Viewing Analytics
- Monitor conversation statistics
- Track user feedback sentiment
- View daily conversation trends
- Check system health status

### Exporting Data
1. Navigate to Conversation Logs
2. Click the Export button
3. Choose CSV or JSON format
4. Download the exported data

## File Structure

```
Team10_image_classifier/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Main dashboard
│   ├── faqs.html         # FAQ listing
│   ├── add_faq.html      # Add FAQ form
│   ├── edit_faq.html     # Edit FAQ form
│   ├── upload.html       # File upload
│   ├── uploads.html      # File listing
│   ├── analytics.html    # Analytics dashboard
│   └── logs.html         # Conversation logs
├── static/
│   └── css/
│       └── style.css     # Custom styles
├── uploads/              # Uploaded files directory
├── test_api.py          # API testing script
└── admin_dashboard.db   # SQLite database (auto-created)
```

## Database Schema

### FAQ Table
- `id`: Primary key
- `question`: FAQ question text
- `answer`: FAQ answer text
- `category`: FAQ category
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `is_active`: Active status flag

### ConversationLog Table
- `id`: Primary key
- `user_question`: User's question
- `bot_response`: System response
- `timestamp`: Conversation timestamp
- `user_feedback`: User feedback (positive/negative/neutral)
- `session_id`: Unique session identifier

### UploadedFile Table
- `id`: Primary key
- `filename`: Original filename
- `file_type`: File type (pdf/csv)
- `upload_date`: Upload timestamp
- `processed`: Processing status
- `content_preview`: Extracted content preview

## Testing

Run the API test script to populate sample data:
```bash
python test_api.py
```

This will:
- Add sample conversation logs
- Test API endpoints
- Verify system functionality

## Security Features

- File type validation (PDF/CSV only)
- File size limits (16MB maximum)
- Secure filename handling
- SQL injection prevention via SQLAlchemy ORM
- CSRF protection with Flask-WTF

## Browser Compatibility

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Team10 Image Classifier system and follows the same licensing terms.

## Support

For issues or questions, please create an issue in the GitHub repository or contact the development team.
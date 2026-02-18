# 🔍 ClaimWatch AI - Insurance Fraud Detection Platform

Advanced AI-powered insurance claim fraud detection system using machine learning to analyze claims and identify suspicious patterns in real-time.

---

## ✨ Features

### 🤖 Intelligent Fraud Detection
- **Machine Learning Model**: Logistic Regression with StandardScaler
- **Real-Time Analysis**: Instantly analyzes claims and provides fraud risk scores
- **6-Feature Detection**: Claims analyzed across multiple risk indicators
- **Probability Scoring**: 0-100% fraud probability for each claim

### 📧 Email Notifications
- **Automatic Alerts**: Applicants receive instant email notifications
- **Decision Status**: Clear "Approved" or "Rejected for Review" messages
- **Claim Details**: Emails include claim type, amount, and risk score
- **Professional Formatting**: HTML emails with branded styling

### 👥 User Management
- **Role-Based Access**: Admin and Analyst accounts
- **User Authentication**: Secure login with password hashing
- **Claim Tracking**: View submitted claims and their status
- **Admin Dashboard**: Monitor all claims, detect trends, and manage team

### 📋 Comprehensive Claim Forms
- **Dynamic Fields**: Forms adapt based on claim type
- **Claim Types**: Auto, Health, Property, Travel, Life
- **Smart Validation**: Client-side and server-side validation
- **Image Upload**: Evidence documentation with file validation (5MB limit, JPG/PNG/GIF)
- **Conditional Fields**: Police report numbers only shown when applicable

### 🎨 Modern User Interface
- **Dark Mode Support**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional Styling**: Blue/teal gradient with modern UI components
- **Pop-up Modals**: Real-time decision notifications
- **Intuitive Navigation**: Clear menu and easy-to-use forms

### 📊 Admin Features
- **Claims Dashboard**: View all claims with filterable data
- **Risk Assessment**: Monitor high-risk claims
- **Team Analytics**: Track claims by team members
- **Fraud Metrics**: Fraud detection ratio and statistics
- **Email Testing**: Test email service directly from admin panel

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Gmail account with App Password (for email notifications)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/claimwatch-ai.git
cd claimwatch-ai
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Email Settings**

Get your Gmail App Password:
- Go to: https://myaccount.google.com/apppasswords
- Select Mail and Windows Computer
- Copy the 16-character password

Set environment variables (Windows PowerShell):
```powershell
[Environment]::SetEnvironmentVariable("MAIL_USERNAME", "your-email@gmail.com", "User")
[Environment]::SetEnvironmentVariable("MAIL_PASSWORD", "xxxx xxxx xxxx xxxx", "User")
[Environment]::SetEnvironmentVariable("MAIL_SERVER", "smtp.gmail.com", "User")
[Environment]::SetEnvironmentVariable("MAIL_PORT", "587", "User")
```

Or run the setup script:
```bash
python setup_email.py
```

5. **Start the Application**
```bash
python app.py
```

6. **Access the App**
- Open browser: http://localhost:5000
- Create an account or log in
- Start submitting claims!

---

## 📁 Project Structure

```
claimwatch-ai/
├── app.py                 # Flask application & routes
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
├── database/
│   ├── db_setup.py      # Database schema & initialization
│   └── db.sqlite3       # SQLite database (auto-created)
│
├── model/
│   ├── train_model.py   # ML model training
│   ├── predict.py       # Model prediction logic
│   └── fraud_model.pkl  # Trained model (auto-created)
│
├── utils/
│   ├── helpers.py       # Email & password utilities
│   ├── preprocessing.py # Data preprocessing for ML
│   └── __init__.py
│
├── templates/           # HTML templates
│   ├── layout.html      # Base layout with footer
│   ├── home.html        # Landing page with contact info
│   ├── login.html       # User login form
│   ├── signup.html      # User registration form
│   ├── dashboard.html   # Main dashboard with help section
│   ├── upload_claim.html # Claim submission form
│   ├── result.html      # Claim decision result with modal
│   ├── claims_history.html # User's claim history
│   └── admin.html       # Admin dashboard
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # All styling + dark mode
│   ├── js/
│   │   ├── script.js    # Form validation & interactions
│   │   └── darkmode.js  # Dark mode toggle
│   └── images/          # App images
│
└── data/                # Data files
    ├── insurance_claims.csv      # Training data
    └── processed_data.csv        # Processed data
```

---

## 🔑 Key Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Landing page with features and contact info |
| `/login` | GET, POST | User login |
| `/signup` | GET, POST | User registration |
| `/dashboard` | GET | Main dashboard with claims overview |
| `/upload-claim` | GET, POST | Submit new claim |
| `/result/<id>` | GET | View claim decision result |
| `/claims-history` | GET | View all user claims |
| `/admin` | GET | Admin dashboard (admin only) |
| `/test-email` | GET | Test email configuration (admin only) |
| `/logout` | GET | User logout |

---

## 💾 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `role`: "admin" or "analyst"

### Claims Table (25+ columns)
- **Personal Info**: claimant_name, claimant_email, claimant_age, claimant_gender
- **Claim Details**: claim_amount, claim_type, incident_date, description
- **Claim-Specific**: Dynamic fields based on claim type
- **Evidence**: claim_image (file path), police_report_number
- **ML Results**: prediction_label, prediction_score
- **Tracking**: email_sent (0 or 1), created_at

---

## 🤖 Machine Learning Model

### Algorithm
- **Type**: Logistic Regression
- **Scaler**: StandardScaler for feature normalization
- **Features**: 6-dimensional feature vector
- **Output**: Binary classification (Legitimate / Fraud)
- **Probability**: Fraud probability (0-1 range)

### Feature Engineering
Features extracted from claim data:
1. Claim amount (normalized)
2. Age of applicant
3. Policy age in days
4. Previous claims count
5. Location risk score
6. Policy-specific indicators

### Training
- Trained on historical insurance claim data
- Cross-validation for model stability
- Continuous improvement with new data

---

## 📧 Email Notifications

### Approved Claims (Legitimate)
```
✓ Status: APPROVED
Claim Type: Health
Claim Amount: $2,000.00
Risk Score: 15.42%

✓ Your claim has been approved and is being processed by our team.
You can expect updates within 5-7 business days.
```

### Rejected Claims (Fraud)
```
⚠ Status: REJECTED FOR REVIEW
Claim Type: Auto
Claim Amount: $50,000.00
Risk Score: 92.18%

⚠ Your claim has been flagged for additional verification.
Our fraud prevention team will review your claim and contact you within 24 hours.
```

### Configuration
- **SMTP Server**: smtp.gmail.com (configurable)
- **Port**: 587 (TLS encryption)
- **From Address**: insuranceclaimwatchai@gmail.com
- **Credentials**: Secure environment variables

---

## 🔒 Security Features

- **Password Hashing**: SHA256-based hashing
- **Session Management**: Flask sessions with secure cookies
- **SMTP TLS**: Encrypted email transmission
- **File Validation**: Type and size validation for uploads
- **CSRF Protection**: Form validation on submission
- **SQL Injection Prevention**: Parameterized queries

---

## 🎨 UI/UX Highlights

### Dark Mode
- Toggle button in top-right corner
- Smooth transitions
- Respects system preferences
- Applies to all pages

### Responsive Design
- Mobile-first approach
- Fluid layouts
- Touch-friendly buttons
- Optimized for all screen sizes

### Accessibility
- Semantic HTML
- Color contrast compliant
- Form labels and validation messages
- Keyboard navigation support

---

## 📞 Contact & Support

📧 **Email**: insuranceclaimwatchai@gmail.com

For assistance with claims, account issues, or feature requests, contact our support team.

**Support Hours**: 24/7 email support with typical response time of 24 hours.

---

## 🤝 Team

**ClaimWatch AI Development Team** - Building the future of fraud detection

---

## 📄 License

This project is proprietary and confidential. All rights reserved.

---

## 🔄 Version History

### v1.0.0 (Current)
- ✅ ML-based fraud detection
- ✅ User authentication
- ✅ Email notifications
- ✅ Admin dashboard
- ✅ Responsive UI with dark mode
- ✅ Image upload and validation
- ✅ Conditional form fields
- ✅ Claims history tracking

---

## 🐛 Troubleshooting

### Email Not Sending
1. Verify MAIL_USERNAME and MAIL_PASSWORD are set
2. Check app password is 16 characters
3. Test with admin panel button: "Test Email Service"
4. Review console logs for error details

### Model Not Loading
1. Ensure `model/fraud_model.pkl` exists
2. Run `python model/train_model.py` to retrain
3. Check all dependencies are installed

### Database Issues
1. Delete `database/db.sqlite3` to reset
2. App will auto-create fresh database on startup
3. Run `python database/db_setup.py` manually if needed

### Port Already in Use
If port 5000 is in use, modify in `app.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change port
```

---

## 📚 Additional Documentation

- [EMAIL_TESTING_GUIDE.md](EMAIL_TESTING_GUIDE.md) - Complete email testing procedures
- [EMAIL_SERVICE_VERIFICATION.md](EMAIL_SERVICE_VERIFICATION.md) - Email service setup details
- [EMAIL_QUICK_REFERENCE.md](EMAIL_QUICK_REFERENCE.md) - Quick email setup guide

---

## 🎯 Future Enhancements

- [ ] Advanced analytics dashboard
- [ ] API endpoints for external integrations
- [ ] Multi-language support
- [ ] SMS notifications
- [ ] Document verification
- [ ] Automated approval workflows
- [ ] Machine learning model retraining pipeline
- [ ] Integration with insurance providers

---

## ⚠️ Important Notes

1. **Development Server**: This uses Flask development server. For production, use WSGI server like Gunicorn
2. **Email Configuration**: Requires valid Gmail account with App Password
3. **Database**: Uses SQLite. For production, use PostgreSQL or MySQL
4. **HTTPS**: Enable HTTPS in production for secure communication
5. **API Keys**: Keep all credentials in environment variables, never commit to version control

---

**Build with ❤️ by the ClaimWatch AI Team**

For questions or contributions, contact insuranceclaimwatchai@gmail.com

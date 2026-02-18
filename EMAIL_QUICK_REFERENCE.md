# Email Service - Quick Reference

## 🚀 Setup Email in 3 Steps

### Step 1: Run Setup Script
```powershell
python setup_email.py
```
- Select your email provider (Gmail recommended)
- Enter credentials
- Test connection automatically

### Step 2: Verify Admin Can Test
- Log in as Admin
- Go to Admin Dashboard
- Click "Test Email Service" button
- See success confirmation

### Step 3: Submit Test Claims
- **Approved**: Health claim $2,000
- **Rejected**: Auto claim $50,000 luxury car
- Check email inbox for both scenarios

---

## 📧 Email Testing Checklist

### Approved Claim Email ✓
- [ ] Green status box
- [ ] "APPROVED" text
- [ ] Claim details (type, amount, risk score)
- [ ] Message: "claim has been approved..."
- [ ] email_sent=1 in database
- [ ] Console shows: `[SUCCESS] Email sent to...`

### Rejected Claim Email ⚠️
- [ ] Red status box
- [ ] "REJECTED FOR REVIEW" text
- [ ] Claim details (type, amount, risk score)
- [ ] Message: "claim requires further review..."
- [ ] email_sent=1 in database
- [ ] Console shows: `[SUCCESS] Email sent to...`

---

## 🔧 Configuration Commands

### Gmail
```powershell
$env:MAIL_USERNAME = "your-email@gmail.com"
$env:MAIL_PASSWORD = "xxxx xxxx xxxx xxxx"  # App Password (16 chars)
$env:MAIL_SERVER = "smtp.gmail.com"
$env:MAIL_PORT = "587"
```

### Office 365
```powershell
$env:MAIL_USERNAME = "your-email@company.com"
$env:MAIL_PASSWORD = "your-password"
$env:MAIL_SERVER = "smtp.office365.com"
$env:MAIL_PORT = "587"
```

### Outlook
```powershell
$env:MAIL_USERNAME = "your-email@outlook.com"
$env:MAIL_PASSWORD = "your-password"
$env:MAIL_SERVER = "smtp-mail.outlook.com"
$env:MAIL_PORT = "587"
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Email not sending | Run `python setup_email.py` to verify credentials |
| Gmail auth fails | Use App Password, not regular password |
| Connection timeout | Check firewall, try different SMTP port |
| Emails in spam | Add sender to contacts, check mail rules |
| Can't find test button | Make sure you're logged in as Admin user |

---

## 📊 Console Log Examples

**Email Sent Successfully:**
```
[INFO] Attempting to send email to john@example.com...
[SUCCESS] Email sent successfully to john@example.com
[SUCCESS] Claim Status: ✓ APPROVED | Amount: $2,000.00
```

**Email Failed - Auth Error:**
```
[ERROR] SMTP authentication failed: ...
[ERROR] Please check MAIL_USERNAME and MAIL_PASSWORD in config
```

**Email Disabled - Credentials Not Set:**
```
[INFO] Email sending disabled: MAIL_USERNAME and MAIL_PASSWORD not configured
```

---

## 🔗 Important Links

- **Gmail App Passwords**: https://myaccount.google.com/apppasswords
- **Gmail Security**: https://myaccount.google.com/security
- **Full Testing Guide**: EMAIL_TESTING_GUIDE.md
- **Email Details**: EMAIL_SERVICE_VERIFICATION.md

---

## 📝 API Reference

### Email Sending Function
```python
from utils.helpers import send_claim_notification

success = send_claim_notification(
    recipient_email="user@example.com",
    claimant_name="John Doe",
    claim_type="Health",
    claim_amount=2000.00,
    prediction_label="Legitimate",  # or "Fraud"
    fraud_probability=15.42
)
# Returns: True if sent, False if failed
```

### Test Email Function
```python
from utils.helpers import test_email_configuration

success = test_email_configuration()
# Sends test email to configured MAIL_USERNAME
# Prints detailed results to console
# Returns: True if successful, False if failed
```

---

## 🚦 Status Indicators

### Email Sending Status in Pop-up Modal
- 🟢 **Green**: Email successfully sent to applicant
- 🔴 **Red**: Email not configured or failed to send
- ⚪ **Gray**: Email service not available

### Database Flag
- `email_sent = 1`: Email was sent successfully
- `email_sent = 0`: Email was not sent (not configured or failed)

---

## 💡 Best Practices

1. **Always test before production**
   - Use `setup_email.py` script
   - Test with approved and rejected claims
   - Verify emails arrive in inbox

2. **Monitor email delivery**
   - Check console logs during submissions
   - Verify `email_sent` flag in database
   - Check spam folders regularly

3. **Secure your credentials**
   - Never commit passwords to version control
   - Use environment variables for all secrets
   - For Gmail, use App Passwords, not your main password

4. **Handle failures gracefully**
   - System continues working even if email fails
   - User sees status indication in modal
   - Full error details logged to console

---

## ✅ Verification Checklist

- [ ] Created app password for email provider
- [ ] Ran `setup_email.py` successfully
- [ ] Test email arrived in inbox
- [ ] Can see "Test Email Service" button on admin page
- [ ] Submitted approved claim and received approval email
- [ ] Submitted rejected claim and received rejection email
- [ ] Both emails show correct claim details
- [ ] Both emails have email_sent=1 in database
- [ ] Console logs show [SUCCESS] messages

Once all checked, your email service is fully operational! 🎉

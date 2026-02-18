# Email Service Testing Guide - ClaimWatch AI

This guide helps you verify that the email notification system is working correctly for both approved and rejected claims.

## 📧 Quick Test (1 min)

### Step 1: Access Admin Dashboard
1. Log in as an **Admin** user
2. Go to the **Admin Dashboard** 
3. Click the green **"✓ Test Email Service"** button in the System Configuration section
4. Check your console logs for the result

**Expected Output:**
```
[INFO] Attempting to send email to your-email@example.com...
[SUCCESS] Email sent successfully to your-email@example.com
[SUCCESS] Email service is working correctly!
```

---

## 📝 Setup Email Credentials

Before testing, you need to configure email credentials. Choose one:

### Option 1: Gmail (Recommended)
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Create App Password: https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer" (or your device)
4. Copy the 16-character password

Set environment variables (Windows):
```powershell
$env:MAIL_USERNAME = "your-email@gmail.com"
$env:MAIL_PASSWORD = "xxxx xxxx xxxx xxxx"  # 16-char app password
```

Or set permanently:
```powershell
[Environment]::SetEnvironmentVariable("MAIL_USERNAME", "your-email@gmail.com", "User")
[Environment]::SetEnvironmentVariable("MAIL_PASSWORD", "xxxx xxxx xxxx xxxx", "User")
```

### Option 2: Custom SMTP Server
```powershell
$env:MAIL_SERVER = "smtp.your-provider.com"
$env:MAIL_PORT = "587"
$env:MAIL_USERNAME = "your-username"
$env:MAIL_PASSWORD = "your-password"
```

### Option 3: Office 365
```powershell
$env:MAIL_SERVER = "smtp.office365.com"
$env:MAIL_PORT = "587"
$env:MAIL_USERNAME = "your-email@company.com"
$env:MAIL_PASSWORD = "your-password"
```

---

## 🧪 Full Email Testing (5 min)

### Test 1: Approved Claim Email ✓

**Goal:** Submit a claim that will be approved (low fraud risk)

1. **Log in** as a regular user (analyst)
2. **Go to Dashboard** → **Submit Claim**
3. **Fill the form with LOW-RISK details:**
   - Claimant Name: John Smith
   - Email: your-email@example.com (must be your real email)
   - Age: 45
   - Gender: Male
   - Claim Type: **Health**
   - Claim Amount: **$2,000**
   - Hospital Name: Mayo Clinic
   - Treatment Type: Routine Checkup
   - Days Hospitalized: 1
   - Pre-existing: No
   - Incident Date: Today
   - Police Report: No
   - Upload Image: (optional)
   - Description: "Regular health checkup at hospital"

4. **Submit the claim**
5. **Check your email inbox** for an email from `noreply@claimwatch.ai`

**Expected Email Content:**
- ✓ Status: **APPROVED** (green background)
- ✓ Claim Type: Health
- ✓ Claim Amount: $2,000.00
- ✓ Risk Score: Should be LOW (< 30%)
- ✓ Message: "Your claim has been approved and is being processed by our team..."

**Also Check:**
- Database: Open `database/db.sqlite3` in SQLite viewer
- Find your claim in `claims` table
- Verify `email_sent = 1` column

**Console Logs Should Show:**
```
[INFO] Attempting to send email to your-email@example.com...
[SUCCESS] Email sent successfully to your-email@example.com
[SUCCESS] Claim Status: ✓ APPROVED | Amount: $2,000.00
```

---

### Test 2: Rejected Claim Email ⚠️

**Goal:** Submit a claim that will be rejected (high fraud risk)

1. **Log in** as a regular user
2. **Go to Dashboard** → **Submit Claim**
3. **Fill the form with HIGH-RISK details:**
   - Claimant Name: John Doe
   - Email: your-email@example.com (same email to verify rejection email)
   - Age: 25
   - Gender: Male
   - Claim Type: **Auto**
   - Claim Amount: **$50,000** (very high amount)
   - Vehicle Make: Luxury Brand (e.g., Ferrari)
   - Vehicle Model: High-end model
   - Vehicle Year: 2024 (very new)
   - Number of Vehicles: 5 (multiple vehicles)
   - Property Damage: Totaled
   - Incident Date: Today
   - Police Report: Yes, enter a fake number (e.g., "POL-2024-99999")
   - Upload Image: (optional)
   - Description: "Complete car destruction, all vehicles in accident"

4. **Submit the claim**
5. **Check your email inbox** for rejection email

**Expected Email Content:**
- ⚠️ Status: **REJECTED FOR REVIEW** (red background)
- ✓ Claim Type: Auto
- ✓ Claim Amount: $50,000.00
- ✓ Risk Score: Should be HIGH (> 70%)
- ✓ Message: "Your claim has been flagged for additional verification..."

**Console Logs Should Show:**
```
[INFO] Attempting to send email to your-email@example.com...
[SUCCESS] Email sent successfully to your-email@example.com
[SUCCESS] Claim Status: ⚠ REJECTED FOR REVIEW | Amount: $50,000.00
```

---

## 🔍 Troubleshooting Email Issues

### Problem: "Email sending disabled: MAIL_USERNAME and MAIL_PASSWORD not configured"

**Solution:**
```powershell
# Check if environment variables are set
$env:MAIL_USERNAME
$env:MAIL_PASSWORD

# If empty, set them:
$env:MAIL_USERNAME = "your-email@gmail.com"
$env:MAIL_PASSWORD = "your-app-password"

# Restart Flask app to pick up new variables
```

### Problem: "SMTP authentication failed"

**Solution:**
1. Verify credentials are correct (copy-paste carefully)
2. For Gmail: Make sure you're using **App Password**, not your regular password
3. Check that 2-Step Verification is enabled
4. Try a different email provider's SMTP settings

### Problem: "Connection timeout"

**Solution:**
1. Check your internet connection
2. Try a different SMTP server:
   - Gmail: `smtp.gmail.com:587`
   - Outlook: `smtp-mail.outlook.com:587`
   - Custom: Check with your email provider
3. Verify firewall isn't blocking SMTP port 587

### Problem: Emails are not arriving in inbox

**Solution:**
1. Check spam/junk folder
2. Check console for success confirmation
3. Verify email address in form has no typos
4. Wait a few minutes (sometimes delayed)
5. Try sending to a different email address

---

## 📊 Email Content Verification Checklist

When you receive an email, verify it contains:

### For Approved Claims ✓
- [ ] Green status box with "✓ APPROVED" 
- [ ] Claim Type is correct
- [ ] Claim Amount matches form (formatted with commas)
- [ ] Risk Score shown as percentage
- [ ] "Your claim has been approved..." message
- [ ] Next action message about 5-7 business days
- [ ] From: noreply@claimwatch.ai
- [ ] Professional formatting with logo area

### For Rejected Claims ⚠️
- [ ] Red status box with "⚠ REJECTED FOR REVIEW"
- [ ] Claim Type is correct
- [ ] Claim Amount matches form
- [ ] Risk Score shown as percentage (high percentage)
- [ ] "Your claim has been flagged..." message
- [ ] Next action message about 24-hour review
- [ ] From: noreply@claimwatch.ai
- [ ] Professional formatting with warning emphasis

---

## 🚀 How Email Works Behind the Scenes

1. **User submits claim** → Form validation
2. **Features extracted** → ML model prediction
3. **Email triggered** → `send_claim_notification()` called with:
   - Recipient email from form
   - Claim details (type, amount)
   - ML prediction result (Legitimate or Fraud)
   - Fraud probability score (0-100%)
4. **Conditional content** → Different HTML generated based on prediction
5. **SMTP sending** → Email sent via configured SMTP server
6. **Database update** → `email_sent=1` flag set for tracking
7. **User sees popup** → Result modal shows decision and email status

---

## 📋 Admin Email Test Features

The admin dashboard includes:
- **System Configuration** section with test button
- **One-click email verification** without submitting a claim
- **Console logging** for debugging SMTP connections
- **Automatic success/failure messages** displayed on admin page

---

## 💡 Pro Tips

1. **Create test Gmail account** for testing (keeps your main inbox clean)
2. **Using localhost?** SMS services won't work; use email only
3. **Batch testing?** Submit 2-3 claims in quick succession to see all email scenarios
4. **Check logs during submit** - Watch the Flask console for email status in real-time
5. **Database inspection** - Use SQLite viewer to confirm `email_sent` flag is set

---

## 📞 Need Help?

Check the console logs for detailed error messages:
- `[INFO]` - Informational messages
- `[SUCCESS]` - Email sent successfully
- `[ERROR]` - Problems that need fixing

All email sending is logged to help diagnose issues.

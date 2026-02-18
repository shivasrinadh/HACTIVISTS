import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def send_claim_notification(recipient_email: str, claimant_name: str, claim_type: str, 
                           claim_amount: float, prediction_label: str, fraud_probability: float) -> bool:
    """
    Send claim decision notification email to applicant
    Optional feature - works if email credentials are configured
    
    Args:
        recipient_email: Recipient's email address
        claimant_name: Name of the claimant
        claim_type: Type of claim (Auto, Health, etc.)
        claim_amount: Claim amount in USD
        prediction_label: Fraud or Legitimate
        fraud_probability: Fraud probability percentage
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Check if email credentials are configured
        if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
            print("[INFO] Email sending disabled: MAIL_USERNAME and MAIL_PASSWORD not configured")
            return False
        
        # Validate email format
        if not recipient_email or '@' not in recipient_email:
            print(f"[ERROR] Invalid email address: {recipient_email}")
            return False
        
        # Create email content
        is_approved = prediction_label == "Legitimate"
        status_text = "✓ APPROVED" if is_approved else "⚠ REJECTED FOR REVIEW"
        subject = f"ClaimWatch AI: Your Claim Decision - {status_text}"
        next_steps = (
            "Your claim has been approved and is being processed by our team. You can expect updates within 5-7 business days."
            if is_approved 
            else "Your claim has been flagged for additional verification. Our fraud prevention team will review your claim and contact you within 24 hours with next steps."
        )
        
        html_body = f"""<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f6fb; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #1d4ed8; padding-bottom: 20px; }}
        .header h1 {{ color: #1d4ed8; margin: 0; font-size: 28px; }}
        .status-box {{ margin: 20px 0; padding: 20px; border-radius: 8px; text-align: center; }}
        .status-approved {{ background-color: #d4edda; border-left: 5px solid #28a745; }}
        .status-rejected {{ background-color: #f8d7da; border-left: 5px solid #dc3545; }}
        .status-text {{ font-size: 20px; font-weight: bold; margin: 0; }}
        .approved {{ color: #155724; }}
        .rejected {{ color: #721c24; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        td {{ padding: 12px; border: 1px solid #ddd; }}
        .label {{ font-weight: bold; background-color: #f9f9f9; width: 40%; }}
        .value {{ color: #333; }}
        .next-steps {{ background-color: #e8efff; border-left: 4px solid #1d4ed8; padding: 15px; border-radius: 4px; margin: 20px 0; }}
        .next-steps p {{ margin: 0; color: #1f2937; }}
        .footer {{ color: #999; font-size: 12px; text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ClaimWatch AI</h1>
            <p style="margin: 5px 0; color: #666;">Claim Decision Notification</p>
        </div>
        
        <p>Dear <strong>{claimant_name}</strong>,</p>
        
        <p style="color: #666;">Your insurance claim has been analyzed by our AI fraud detection system. Below are the details of your claim decision:</p>
        
        <div class="status-box {'status-approved' if is_approved else 'status-rejected'}">
            <p class="status-text {'approved' if is_approved else 'rejected'}">{status_text}</p>
        </div>
        
        <table>
            <tr>
                <td class="label">Claim Type:</td>
                <td class="value">{claim_type}</td>
            </tr>
            <tr>
                <td class="label">Claim Amount:</td>
                <td class="value">${claim_amount:,.2f}</td>
            </tr>
            <tr>
                <td class="label">Risk Assessment Score:</td>
                <td class="value">{fraud_probability:.2f}%</td>
            </tr>
            <tr>
                <td class="label">Decision:</td>
                <td class="value"><strong>{status_text}</strong></td>
            </tr>
        </table>
        
        <div class="next-steps">
            <p><strong>What happens next?</strong></p>
            <p>{next_steps}</p>
        </div>
        
        <p style="color: #666; font-size: 14px; line-height: 1.6;">
            If you have any questions about this decision or need to provide additional information, 
            please reply to this email or contact our customer support team at support@claimwatch.ai
        </p>
        
        <div class="footer">
            <p>© 2026 ClaimWatch AI. All rights reserved.</p>
            <p>This is an automated message. Please do not reply with sensitive information.</p>
        </div>
    </div>
</body>
</html>"""
        
        # Create and send message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = Config.MAIL_DEFAULT_SENDER
        msg["To"] = recipient_email
        msg.attach(MIMEText(html_body, "html"))
        
        # Send via SMTP
        print(f"[INFO] Attempting to send email to {recipient_email}...")
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"[SUCCESS] Email sent successfully to {recipient_email}")
        print(f"[SUCCESS] Claim Status: {status_text} | Amount: ${claim_amount:,.2f}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERROR] SMTP authentication failed: {str(e)}")
        print(f"[ERROR] Please check MAIL_USERNAME and MAIL_PASSWORD in config")
        return False
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP error while sending to {recipient_email}: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send email to {recipient_email}: {str(e)}")
        return False


def test_email_configuration() -> bool:
    """
    Test email configuration by sending a test email
    Returns True if test email sent successfully, False otherwise
    """
    try:
        if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
            print("[ERROR] Email credentials not configured")
            print("[INFO] Set MAIL_USERNAME and MAIL_PASSWORD environment variables")
            return False
        
        test_email = Config.MAIL_USERNAME
        print(f"[INFO] Testing email configuration with {test_email}...")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "ClaimWatch AI - Email Configuration Test"
        msg["From"] = Config.MAIL_DEFAULT_SENDER
        msg["To"] = test_email
        
        html_body = """<html><body style="font-family: Arial, sans-serif;">
            <h2 style="color: #1d4ed8;">ClaimWatch AI - Email Test</h2>
            <p>This is a test email to verify your email configuration is working correctly.</p>
            <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #155724; margin: 0;"><strong>✓ Email service is configured correctly!</strong></p>
            </div>
            <p>You can now send claim notifications to applicants.</p>
        </body></html>"""
        
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"[SUCCESS] Test email sent successfully to {test_email}")
        print("[SUCCESS] Email service is working correctly!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Email test failed: {str(e)}")
        return False

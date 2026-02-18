#!/usr/bin/env python3
"""
Quick Email Setup - Configure credentials directly
"""
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("\n" + "="*60)
print("  ClaimWatch AI - Quick Email Setup")
print("="*60 + "\n")

gmail = input("Enter your Gmail address (e.g. claimwatchai@gmail.com): ").strip()
app_password = input("Enter your 16-character App Password (with spaces): ").strip()

if not gmail or '@gmail.com' not in gmail:
    print("❌ Invalid Gmail address")
    exit(1)

if len(app_password.replace(" ", "")) != 16:
    print("❌ Invalid password (should be 16 characters)")
    exit(1)

print("\n" + "-"*60)
print("Setting up configuration...")
print("-"*60 + "\n")

# Set environment variables
config = {
    "MAIL_USERNAME": gmail,
    "MAIL_PASSWORD": app_password,
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": "587",
}

os.environ.update(config)

# Set permanently in Windows
try:
    for key, value in config.items():
        value_escaped = f'"{value}"' if ' ' in value else value
        subprocess.run(f'setx {key} {value_escaped}', shell=True, capture_output=True, timeout=5)
        print(f"✓ Set {key}")
except Exception as e:
    print(f"⚠️  Warning: {e}")

print("\n" + "-"*60)
print("Testing Email Connection...")
print("-"*60 + "\n")

try:
    # Test SMTP connection
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
        print("✓ Connected to Gmail SMTP")
        server.starttls()
        print("✓ Started TLS encryption")
        server.login(gmail, app_password)
        print("✓ Authentication successful!")
        
        # Send test email
        print("\n" + "-"*60)
        print("Sending Test Email...")
        print("-"*60 + "\n")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "ClaimWatch AI - Email Test ✓"
        msg["From"] = gmail
        msg["To"] = gmail
        
        html = """<html><body style="font-family: Arial, sans-serif;">
            <h2 style="color: #1d4ed8;">✓ ClaimWatch AI Email Test</h2>
            <p>Your email is configured correctly!</p>
            <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="color: #155724;"><strong>✓ Email service is working!</strong></p>
                <p>The app can now send claim notifications.</p>
            </div>
            <p style="color: #666; font-size: 13px;">From: ClaimWatch AI</p>
        </body></html>"""
        
        msg.attach(MIMEText(html, "html"))
        server.send_message(msg)
        
        print(f"✓ Test email sent to {gmail}")
        print("\n" + "="*60)
        print("✅ Success! Email is configured and working!")
        print("="*60)
        print("\nYou can now:")
        print("1. Go to http://localhost:5000")
        print("2. Log in and submit claims")
        print("3. Emails will be sent from: " + gmail)
        print("4. Check your inbox for claim notifications")
        
except smtplib.SMTPAuthenticationError as e:
    print(f"\n❌ Authentication failed: {e}")
    print("Check your Gmail address and app password")
    exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    exit(1)

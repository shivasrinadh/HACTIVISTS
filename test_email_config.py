import smtplib
import os
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'insuranceclaimwatchai@gmail.com'
password = 'Shiva@15'

print('\n' + '='*60)
print('  ClaimWatch AI - Email Configuration Test')
print('='*60 + '\n')

print('[INFO] Testing Gmail connection with your credentials...')
print(f'[INFO] Email: {email}')

try:
    print('[...] Connecting to smtp.gmail.com:587')
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    print('[✓] Connected to Gmail SMTP')
    
    server.starttls()
    print('[✓] TLS encryption started')
    
    server.login(email, password)
    print('[✓] Authentication successful!')
    
    # Send test email
    print('\n[INFO] Sending test email...')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'ClaimWatch AI - Email Test ✓'
    msg['From'] = email
    msg['To'] = email
    
    html = """<html><body style="font-family: Arial, sans-serif;">
        <h2 style="color: #1d4ed8;">✓ ClaimWatch AI Email Test</h2>
        <div style="background-color: #d4edda; padding: 15px; border-radius: 8px;">
            <p style="color: #155724;"><strong>✓ Email service is working!</strong></p>
            <p>Your app can now send claim notifications.</p>
        </div>
        <p style="color: #666; font-size: 12px;">From: ClaimWatch AI</p>
    </body></html>"""
    
    msg.attach(MIMEText(html, 'html'))
    server.send_message(msg)
    print('[✓] Test email sent!')
    server.quit()
    
    # Set environment variables
    print('\n[INFO] Saving credentials to system...')
    config = {
        'MAIL_USERNAME': email,
        'MAIL_PASSWORD': password,
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': '587',
    }
    
    for key, value in config.items():
        os.environ[key] = value
        value_masked = '*' * len(value) if 'PASSWORD' in key else value
        print(f'[✓] {key} = {value_masked}')
    
    # Set permanently
    print('\n[INFO] Setting permanent environment variables...')
    for key, value in config.items():
        value_escaped = f'"{value}"' if ' ' in value else value
        subprocess.run(f'setx {key} {value_escaped}', shell=True, capture_output=True, timeout=5)
    
    print('\n' + '='*60)
    print('✅ SUCCESS! Email is configured and working!')
    print('='*60)
    print('\n📧 Email Details:')
    print(f'  From: {email}')
    print('  Server: smtp.gmail.com:587')
    print('  Status: ✓ Connected and authenticated')
    print('\nCheck your inbox at ' + email + ' for the test email!')
    print('\nYou can now:')
    print('  1. Start the app: python app.py')
    print('  2. Go to http://localhost:5000')
    print('  3. Log in and submit claims')
    print('  4. Emails will be sent automatically!')
    
except smtplib.SMTPAuthenticationError as e:
    print(f'\n❌ Authentication failed: {e}')
    print('\nThe password might be incorrect or Gmail security is blocking it.')
    print('Try using an App Password from: https://myaccount.google.com/apppasswords')
    exit(1)
except Exception as e:
    print(f'\n❌ Error: {e}')
    exit(1)

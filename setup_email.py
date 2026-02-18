#!/usr/bin/env python3
"""
Setup Email Credentials for ClaimWatch AI
This script helps configure SMTP credentials for sending claim notification emails.
"""

import os
import sys
from pathlib import Path


def print_header():
    print("\n" + "="*60)
    print("  ClaimWatch AI - Email Service Configuration")
    print("="*60 + "\n")


def get_email_provider():
    """Ask user to select email provider"""
    providers = {
        "1": ("Gmail", "smtp.gmail.com", "587"),
        "2": ("Office 365", "smtp.office365.com", "587"),
        "3": ("Outlook", "smtp-mail.outlook.com", "587"),
        "4": ("Custom", None, None),
    }
    
    print("Select your email provider:")
    for key, (name, _, _) in providers.items():
        print(f"  {key}. {name}")
    print("  0. Skip email setup")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    if choice == "0":
        return None
    
    if choice not in providers:
        print("Invalid choice. Please enter 0-4.")
        return get_email_provider()
    
    return providers[choice]


def setup_gmail():
    """Setup Gmail configuration"""
    print("\n" + "-"*60)
    print("GMAIL SETUP")
    print("-"*60)
    print("\nGmail requires an 'App Password' for third-party apps.")
    print("\nSteps:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Select 'Mail' and 'Windows Computer' (or your device)")
    print("3. Google will generate a 16-character password")
    print("4. Copy it and paste below (including spaces)\n")
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your 16-character App Password: ").strip()
    
    if not email or "@gmail.com" not in email:
        print("❌ Invalid Gmail address")
        return None
    
    if len(app_password.replace(" ", "")) != 16:
        print("❌ Invalid App Password (should be 16 characters)")
        return None
    
    return {
        "MAIL_SERVER": "smtp.gmail.com",
        "MAIL_PORT": "587",
        "MAIL_USERNAME": email,
        "MAIL_PASSWORD": app_password,
    }


def setup_office365():
    """Setup Office 365 configuration"""
    print("\n" + "-"*60)
    print("OFFICE 365 SETUP")
    print("-"*60)
    
    email = input("Enter your Office 365 email: ").strip()
    password = input("Enter your Office 365 password: ").strip()
    
    if not email or "@" not in email:
        print("❌ Invalid email address")
        return None
    
    if not password:
        print("❌ Password cannot be empty")
        return None
    
    return {
        "MAIL_SERVER": "smtp.office365.com",
        "MAIL_PORT": "587",
        "MAIL_USERNAME": email,
        "MAIL_PASSWORD": password,
    }


def setup_outlook():
    """Setup Outlook configuration"""
    print("\n" + "-"*60)
    print("OUTLOOK SETUP")
    print("-"*60)
    
    email = input("Enter your Outlook email: ").strip()
    password = input("Enter your Outlook password: ").strip()
    
    if not email or "@outlook.com" not in email and "@hotmail.com" not in email:
        print("❌ Invalid Outlook email address")
        return None
    
    if not password:
        print("❌ Password cannot be empty")
        return None
    
    return {
        "MAIL_SERVER": "smtp-mail.outlook.com",
        "MAIL_PORT": "587",
        "MAIL_USERNAME": email,
        "MAIL_PASSWORD": password,
    }


def setup_custom():
    """Setup custom email provider"""
    print("\n" + "-"*60)
    print("CUSTOM SMTP SERVER")
    print("-"*60)
    print("\nFor your email provider, you need:")
    print("- SMTP Server address")
    print("- SMTP Port (usually 587 for TLS)")
    print("- Username (usually your email)")
    print("- Password (usually your password)\n")
    
    server = input("Enter SMTP server address: ").strip()
    port = input("Enter SMTP port (usually 587): ").strip()
    username = input("Enter SMTP username: ").strip()
    password = input("Enter SMTP password: ").strip()
    
    if not all([server, port, username, password]):
        print("❌ All fields are required")
        return None
    
    try:
        int(port)
    except ValueError:
        print("❌ Port must be a number")
        return None
    
    return {
        "MAIL_SERVER": server,
        "MAIL_PORT": port,
        "MAIL_USERNAME": username,
        "MAIL_PASSWORD": password,
    }


def set_windows_env_vars(config):
    """Set environment variables in Windows"""
    print("\n" + "-"*60)
    print("Setting Environment Variables")
    print("-"*60 + "\n")
    
    # Try to set via Python's os.environ (temporary for current session)
    os.environ.update(config)
    
    # Also try to set permanently for future sessions
    try:
        import subprocess
        for key, value in config.items():
            # Escape password if it contains special characters
            value_escaped = f'"{value}"' if '"' in value or ' ' in value else value
            cmd = f'setx {key} {value_escaped}'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            print(f"✓ Set {key}")
        
        print("\n✅ Environment variables set!")
        print("   (You may need to restart your terminal for changes to take effect)")
    except Exception as e:
        print(f"⚠️  Could not set permanent env vars: {e}")
        print("   Variables are set for current session only")


def test_configuration():
    """Test the email configuration"""
    print("\n" + "-"*60)
    print("Testing Configuration")
    print("-"*60 + "\n")
    
    from config import Config
    import smtplib
    
    print(f"SMTP Server: {Config.MAIL_SERVER}")
    print(f"SMTP Port: {Config.MAIL_PORT}")
    print(f"Username: {Config.MAIL_USERNAME}")
    print(f"Password: {'*' * len(Config.MAIL_PASSWORD) if Config.MAIL_PASSWORD else 'NOT SET'}")
    
    if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
        print("\n⚠️  Email credentials not configured. Please run this script again.")
        return False
    
    print("\nAttempting to connect to SMTP server...\n")
    
    try:
        with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT, timeout=10) as server:
            print("✓ Successfully connected to SMTP server")
            
            server.starttls()
            print("✓ Successfully started TLS encryption")
            
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            print("✓ Successfully authenticated with credentials")
            
        print("\n✅ Email configuration is correct!")
        print("   You can now send claim notification emails.")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("\n❌ Authentication failed!")
        print("   Check your username and password.")
        return False
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        return False


def main():
    """Main setup flow"""
    print_header()
    
    provider = get_email_provider()
    
    if provider is None:
        print("Setup cancelled.")
        return
    
    name, default_server, default_port = provider
    
    if name == "Gmail":
        config = setup_gmail()
    elif name == "Office 365":
        config = setup_office365()
    elif name == "Outlook":
        config = setup_outlook()
    else:  # Custom
        config = setup_custom()
    
    if config is None:
        print("\n❌ Setup failed. Please try again.")
        return
    
    print("\n" + "="*60)
    print("Configuration Summary")
    print("="*60)
    for key, value in config.items():
        if "PASSWORD" in key:
            display_value = "*" * len(value) if value else "NOT SET"
        else:
            display_value = value
        print(f"{key}: {display_value}")
    
    confirm = input("\nDoes this look correct? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print("Setup cancelled.")
        return
    
    # Set environment variables
    set_windows_env_vars(config)
    
    # Test the configuration
    input("\nPress Enter to test the configuration...")
    test_configuration()
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Submit claims to test email notifications")
    print("2. Use the 'Test Email Service' button in Admin Dashboard")
    print("3. Check your emails for received notifications")
    print("\nFor help, see: EMAIL_TESTING_GUIDE.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

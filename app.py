from datetime import datetime
from functools import wraps
import sqlite3
import os
from pathlib import Path
from werkzeug.utils import secure_filename

from flask import Flask, g, redirect, render_template, request, session, url_for, flash

from config import Config
from database.db_setup import init_db
from model.predict import ensure_model_exists, predict_claim
from utils.helpers import hash_password, verify_password, send_claim_notification, test_email_configuration
from utils.preprocessing import prepare_features_from_form


app = Flask(__name__)
app.config.from_object(Config)

# File upload configuration
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Create upload folder if it doesn't exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return view(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        db = get_db()
        user = db.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if user and verify_password(password, user["password_hash"]):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash("Welcome back.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid credentials.", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "analyst").strip()

        db = get_db()

        # Validation
        if not username:
            flash("Username is required.", "danger")
            return render_template("signup.html")

        if not password:
            flash("Password is required.", "danger")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("signup.html")

        # Check if username already exists
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return render_template("signup.html")

        # Create new user
        try:
            password_hash = hash_password(password)
            db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            db.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as exc:
            flash(f"Error creating account: {str(exc)}", "danger")
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    if session.get("role") == "admin":
        total_claims = db.execute("SELECT COUNT(*) AS count FROM claims").fetchone()["count"]
        flagged_claims = db.execute(
            "SELECT COUNT(*) AS count FROM claims WHERE prediction_label = 'Fraud'"
        ).fetchone()["count"]
        recent_claims = db.execute(
            """
            SELECT c.id, c.claimant_name, c.claim_amount, c.prediction_label, c.prediction_score,
                   c.created_at, u.username
            FROM claims c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
            LIMIT 8
            """
        ).fetchall()
    else:
        total_claims = db.execute(
            "SELECT COUNT(*) AS count FROM claims WHERE user_id = ?", (session["user_id"],)
        ).fetchone()["count"]
        flagged_claims = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM claims
            WHERE user_id = ? AND prediction_label = 'Fraud'
            """,
            (session["user_id"],),
        ).fetchone()["count"]
        recent_claims = db.execute(
            """
            SELECT id, claimant_name, claim_amount, prediction_label, prediction_score, created_at
            FROM claims
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 8
            """,
            (session["user_id"],),
        ).fetchall()

    safe_claims = total_claims - flagged_claims
    fraud_rate = (flagged_claims / total_claims * 100) if total_claims else 0

    return render_template(
        "dashboard.html",
        total_claims=total_claims,
        flagged_claims=flagged_claims,
        safe_claims=safe_claims,
        fraud_rate=fraud_rate,
        recent_claims=recent_claims,
    )


@app.route("/upload_claim", methods=["GET", "POST"])
@login_required
def upload_claim():
    if request.method == "POST":
        form_data = {
            "claimant_name": request.form.get("claimant_name", "").strip(),
            "claimant_email": request.form.get("claimant_email", "").strip(),
            "claimant_age": request.form.get("claimant_age", ""),
            "claimant_gender": request.form.get("claimant_gender", "").strip(),
            "claim_type": request.form.get("claim_type", "").strip(),
            "incident_date": request.form.get("incident_date", "").strip(),
            "claim_amount": request.form.get("claim_amount", ""),
            "description": request.form.get("description", "").strip(),
            "age_of_policy_days": request.form.get("age_of_policy_days", ""),
            "number_of_previous_claims": request.form.get("number_of_previous_claims", ""),
            "location_risk_score": request.form.get("location_risk_score", ""),
            "police_report_filed": request.form.get("police_report_filed", "0"),
            "police_report_number": request.form.get("police_report_number", "").strip(),
            "witnesses": request.form.get("witnesses", ""),
        }

        # Handle image upload
        image_filename = None
        if 'claim_image' in request.files:
            file = request.files['claim_image']
            if file and file.filename != '':
                # Validate file
                if not allowed_file(file.filename):
                    flash("Invalid file type. Only JPG, PNG, and GIF files are allowed.", "danger")
                    return render_template("upload_claim.html", form_data=form_data)
                
                # Check file size
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0)
                
                if file_length > MAX_FILE_SIZE:
                    flash("File size exceeds 5MB limit.", "danger")
                    return render_template("upload_claim.html", form_data=form_data)
                
                # Save file with secure filename
                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_")
                image_filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        try:
            features = prepare_features_from_form(form_data)
            prediction_label, prediction_score = predict_claim(features)
        except ValueError as exc:
            flash(str(exc), "danger")
            return render_template("upload_claim.html", form_data=form_data)

        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO claims (
                user_id, claimant_name, claimant_email, claimant_age, claimant_gender, claim_amount, claim_type, incident_date, description,
                claim_image, age_of_policy_days, number_of_previous_claims, location_risk_score,
                police_report_filed, police_report_number, witnesses, prediction_label, prediction_score, email_sent, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                form_data["claimant_name"],
                form_data["claimant_email"],
                int(form_data["claimant_age"]) if form_data["claimant_age"] else None,
                form_data["claimant_gender"],
                features["claim_amount"],
                form_data["claim_type"],
                form_data["incident_date"],
                form_data["description"],
                image_filename,
                features["age_of_policy_days"],
                features["number_of_previous_claims"],
                features["location_risk_score"],
                features["police_report_filed"],
                form_data["police_report_number"] if form_data["police_report_filed"] == "1" else None,
                features["witnesses"],
                prediction_label,
                float(prediction_score),
                0,  # email_sent initially 0
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        db.commit()
        claim_id = cursor.lastrowid
        
        # Send notification email to applicant (optional - only if configured)
        email_sent = send_claim_notification(
            recipient_email=form_data["claimant_email"],
            claimant_name=form_data["claimant_name"],
            claim_type=form_data["claim_type"],
            claim_amount=features["claim_amount"],
            prediction_label=prediction_label,
            fraud_probability=float(prediction_score) * 100
        )
        
        # Update email_sent status in database if email was sent
        if email_sent:
            db.execute("UPDATE claims SET email_sent = 1 WHERE id = ?", (claim_id,))
            db.commit()
            flash("Claim submitted successfully. Notification email sent.", "success")
        else:
            flash("Claim submitted successfully.", "success")

        return redirect(url_for("result", claim_id=claim_id))

    return render_template("upload_claim.html", form_data={})


@app.route("/result/<int:claim_id>")
@login_required
def result(claim_id):
    db = get_db()
    query = "SELECT * FROM claims WHERE id = ?"
    params = [claim_id]
    if session.get("role") != "admin":
        query += " AND user_id = ?"
        params.append(session["user_id"])

    claim = db.execute(query, tuple(params)).fetchone()
    if not claim:
        flash("Claim not found.", "warning")
        return redirect(url_for("claims_history"))

    return render_template("result.html", claim=claim)


@app.route("/claims_history")
@login_required
def claims_history():
    db = get_db()
    if session.get("role") == "admin":
        claims = db.execute(
            """
            SELECT c.id, c.claimant_name, c.claim_amount, c.claim_type, c.prediction_label,
                   c.prediction_score, c.created_at, u.username
            FROM claims c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.created_at DESC
            """
        ).fetchall()
    else:
        claims = db.execute(
            """
            SELECT id, claimant_name, claim_amount, claim_type, prediction_label,
                   prediction_score, created_at
            FROM claims
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (session["user_id"],),
        ).fetchall()

    return render_template("claims_history.html", claims=claims)


@app.route("/admin")
@login_required
@admin_required
def admin():
    db = get_db()
    user_count = db.execute("SELECT COUNT(*) AS count FROM users").fetchone()["count"]
    claim_count = db.execute("SELECT COUNT(*) AS count FROM claims").fetchone()["count"]
    fraud_count = db.execute(
        "SELECT COUNT(*) AS count FROM claims WHERE prediction_label = 'Fraud'"
    ).fetchone()["count"]

    users = db.execute(
        """
        SELECT u.username, u.role, COUNT(c.id) AS claims_submitted
        FROM users u
        LEFT JOIN claims c ON c.user_id = u.id
        GROUP BY u.id
        ORDER BY claims_submitted DESC, u.username ASC
        """
    ).fetchall()

    high_risk_claims = db.execute(
        """
        SELECT id, claimant_name, claim_amount, prediction_score, created_at
        FROM claims
        WHERE prediction_label = 'Fraud'
        ORDER BY prediction_score DESC
        LIMIT 10
        """
    ).fetchall()

    return render_template(
        "admin.html",
        user_count=user_count,
        claim_count=claim_count,
        fraud_count=fraud_count,
        users=users,
        high_risk_claims=high_risk_claims,
    )


def bootstrap():
    init_db()
    ensure_model_exists()


@app.route("/test-email")
@login_required
@admin_required
def test_email_route():
    """Test email configuration by sending a test email"""
    success = test_email_configuration()
    
    if success:
        flash("✓ Test email sent successfully! Email service is working.", "success")
    else:
        flash("✗ Test email failed. Check console logs for error details.", "danger")
    
    return redirect(url_for("admin"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve uploaded claim images"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    # Security: ensure file exists and is in upload folder
    if not os.path.exists(file_path):
        flash("Image not found.", "warning")
        return redirect(url_for("dashboard"))
    
    from flask import send_file
    try:
        return send_file(file_path)
    except Exception:
        flash("Error retrieving image.", "danger")
        return redirect(url_for("dashboard"))


bootstrap()


if __name__ == "__main__":
    app.run(debug=True)

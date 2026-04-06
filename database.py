from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    job_url = db.Column(db.String(500), default='')
    status = db.Column(db.String(50), default='Applied')
    contact_name = db.Column(db.String(200), default='')
    contact_email = db.Column(db.String(200), default='')
    notes = db.Column(db.Text, default='')
    date_applied = db.Column(db.Date, default=date.today)
    # Cybersecurity-specific fields
    clearance = db.Column(db.String(100), default='None')
    certs_required = db.Column(db.String(300), default='')
    work_type = db.Column(db.String(50), default='On-site')
    sector = db.Column(db.String(100), default='')

class TargetCompany(db.Model):
    __tablename__ = 'target_companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100), default='')
    location = db.Column(db.String(200), default='Las Vegas, NV')
    careers_url = db.Column(db.String(500), default='')
    notes = db.Column(db.Text, default='')
    priority = db.Column(db.String(20), default='Medium')  # High / Medium / Low
    watching = db.Column(db.Boolean, default=True)

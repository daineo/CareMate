from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Elderly(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    emergency_contact = db.Column(db.String(50), nullable=False)
    health_data = db.relationship('HealthData', backref='elderly', lazy=True)

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elderly_id = db.Column(db.Integer, db.ForeignKey('elderly.id'), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class TaskReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elderly_id = db.Column(db.Integer, db.ForeignKey('elderly.id'), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    task_time = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(200), nullable=False)
    verified = db.Column(db.Boolean, default=False)

class EmergencyAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elderly_id = db.Column(db.Integer, db.ForeignKey('elderly.id'), nullable=False)
    alert_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)

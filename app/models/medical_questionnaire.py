from app import db
from datetime import datetime

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Chronic Conditions
    has_heart_disease = db.Column(db.Boolean, default=False)
    has_diabetes = db.Column(db.Boolean, default=False)
    has_asthma = db.Column(db.Boolean, default=False)
    has_cancer = db.Column(db.Boolean, default=False)
    has_hypertension = db.Column(db.Boolean, default=False)
    has_arthritis = db.Column(db.Boolean, default=False)
    other_conditions = db.Column(db.Text)
    
    # Additional Info
    additional_notes = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    surgeries = db.relationship('Surgery', backref='medical_history', lazy=True)
    medications = db.relationship('Medication', backref='medical_history', lazy=True)
    allergies = db.relationship('Allergy', backref='medical_history', lazy=True)
    immunizations = db.relationship('Immunization', backref='medical_history', lazy=True)

class Surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('medical_history.id'), nullable=False)
    procedure_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date)
    hospital = db.Column(db.String(200))
    surgeon = db.Column(db.String(200))
    notes = db.Column(db.Text)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('medical_history.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    reason = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_current = db.Column(db.Boolean, default=True)

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('medical_history.id'), nullable=False)
    allergen = db.Column(db.String(200), nullable=False)
    reaction = db.Column(db.String(200))
    severity = db.Column(db.String(50))  # Mild, Moderate, Severe
    diagnosed_date = db.Column(db.Date)

class Immunization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('medical_history.id'), nullable=False)
    vaccine_name = db.Column(db.String(200), nullable=False)
    date_administered = db.Column(db.Date)
    provider = db.Column(db.String(200))
    lot_number = db.Column(db.String(100))
    next_due_date = db.Column(db.Date)

class FamilyHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Family Conditions
    has_family_heart_disease = db.Column(db.Boolean, default=False)
    has_family_diabetes = db.Column(db.Boolean, default=False)
    has_family_cancer = db.Column(db.Boolean, default=False)
    has_family_hypertension = db.Column(db.Boolean, default=False)
    has_family_mental_illness = db.Column(db.Boolean, default=False)
    other_family_conditions = db.Column(db.Text)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    family_members = db.relationship('FamilyMember', backref='family_history', lazy=True)

class FamilyMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    family_history_id = db.Column(db.Integer, db.ForeignKey('family_history.id'), nullable=False)
    relationship = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    living_status = db.Column(db.String(50))  # Living, Deceased
    medical_conditions = db.Column(db.Text)
    cause_of_death = db.Column(db.String(200))
    age_at_death = db.Column(db.Integer)

class LifestyleFactors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Smoking
    smoking_status = db.Column(db.String(50))  # Never, Former, Current
    packs_per_day = db.Column(db.Float)
    years_smoked = db.Column(db.Integer)
    quit_date = db.Column(db.Date)
    
    # Alcohol
    alcohol_consumption = db.Column(db.String(50))  # Never, Occasional, Moderate, Heavy
    drinks_per_week = db.Column(db.Integer)
    
    # Exercise
    exercise_frequency = db.Column(db.String(50))  # Never, 1-2/week, 3-4/week, 5+/week
    exercise_types = db.Column(db.String(200))
    exercise_duration = db.Column(db.Integer)  # minutes per session
    
    # Diet
    diet_type = db.Column(db.String(100))  # Regular, Vegetarian, Vegan, etc.
    daily_water_intake = db.Column(db.Integer)  # cups
    dietary_restrictions = db.Column(db.Text)
    
    # Sleep
    average_sleep_hours = db.Column(db.Float)
    sleep_quality = db.Column(db.String(50))  # Poor, Fair, Good, Excellent
    sleep_disorders = db.Column(db.Text)
    
    # Stress
    stress_level = db.Column(db.String(50))  # Low, Moderate, High
    stress_management = db.Column(db.Text)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
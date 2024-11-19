from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for physician-patient relationship
physician_patients = db.Table('physician_patients',
    db.Column('physician_id', db.Integer, db.ForeignKey('user.id', name='fk_physician_patients_physician')),
    db.Column('patient_id', db.Integer, db.ForeignKey('user.id', name='fk_physician_patients_patient'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User type flags
    is_physician = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Profile Information
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    
    # Emergency Contact Information
    emergency_contact_name = db.Column(db.String(120))
    emergency_contact_relationship = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))
    
    # Insurance Information
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    insurance_group_number = db.Column(db.String(50))
    
    # Medical Information
    medical_history = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    family_history = db.Column(db.Text)
    lifestyle_info = db.Column(db.Text)
    has_completed_questionnaire = db.Column(db.Boolean, default=False)
    
    # Physician-specific fields
    physician_type = db.Column(db.String(20))
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Document(db.Model):
    __tablename__ = 'document'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_document_user'), nullable=False)
    uploading_physician_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_document_physician'))
    
    # Relationships
    patient = db.relationship('User', foreign_keys=[user_id], backref=db.backref('documents', lazy='dynamic'))
    uploading_physician = db.relationship('User', foreign_keys=[uploading_physician_id], 
                                        backref=db.backref('uploaded_documents', lazy='dynamic'))

class DocumentRequest(db.Model):
    __tablename__ = 'document_request'
    
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    
    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_document_request_patient'), nullable=False)
    requesting_physician_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_document_request_physician'), nullable=False)
    
    # Relationships
    patient = db.relationship('User', foreign_keys=[patient_id], 
                            backref=db.backref('document_requests_received', lazy='dynamic'))
    requesting_physician = db.relationship('User', foreign_keys=[requesting_physician_id], 
                                         backref=db.backref('document_requests_sent', lazy='dynamic'))

    def __repr__(self):
        return f"DocumentRequest('{self.document_type}', requested at {self.requested_at})"
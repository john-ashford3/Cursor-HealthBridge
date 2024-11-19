from app import create_app, db
from app.models.user import (
    User, Document, DocumentRequest,
    physician_patients  # Changed from physician_patient
)

app = create_app()

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Create admin user
    admin = User(
        name='Admin User',
        email='admin@example.com',
        password='your-hashed-password-here',  # You should hash this
        is_admin=True,
        is_verified=True
    )
    
    # Create test physician
    physician = User(
        name='Dr. John Smith',
        email='doctor@example.com',
        password='your-hashed-password-here',  # You should hash this
        is_physician=True,
        is_verified=True,
        physician_type='both',
        specialization='General Practice',
        license_number='12345'
    )
    
    # Create test patient
    patient = User(
        name='Jane Doe',
        email='patient@example.com',
        password='your-hashed-password-here',  # You should hash this
        is_verified=True
    )
    
    # Add users to database
    db.session.add(admin)
    db.session.add(physician)
    db.session.add(patient)
    
    # Commit changes
    db.session.commit()
    
    print("Database initialized!")
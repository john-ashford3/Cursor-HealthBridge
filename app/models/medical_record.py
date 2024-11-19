from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Text
from flask import current_app
import os

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)  # Size in bytes
    mime_type = db.Column(db.String(100))
    azure_url = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    shared_with = db.Column(db.JSON, default=list)  # Store as JSON for SQLite compatibility

    # Define categories as class variables for consistency
    CATEGORIES = [
        ('general', 'General Records'),
        ('lab_results', 'Laboratory Results'),
        ('imaging', 'Imaging & X-Rays'),
        ('prescriptions', 'Prescriptions'),
        ('vaccinations', 'Vaccinations'),
        ('surgical', 'Surgical Records'),
        ('dental', 'Dental Records'),
        ('mental_health', 'Mental Health Records'),
        ('other', 'Other Documents')
    ]

    @property
    def file_path(self):
        """Get the local file path."""
        return os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            str(self.user_id),
            self.filename
        )

    @property
    def download_url(self):
        """Get the appropriate download URL."""
        if self.azure_url:
            return self.azure_url
        return None  # Local download will be handled by the download route

    def is_shared_with(self, user_id):
        """Check if document is shared with a specific user."""
        return str(user_id) in (self.shared_with or [])

    def share_with(self, user_id):
        """Share document with a user."""
        if self.shared_with is None:
            self.shared_with = []
        if str(user_id) not in self.shared_with:
            self.shared_with.append(str(user_id))

    def unshare_with(self, user_id):
        """Unshare document with a user."""
        if self.shared_with and str(user_id) in self.shared_with:
            self.shared_with.remove(str(user_id))

class DocumentShare(db.Model):
    """Advanced sharing model with expiration and permissions."""
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    access_level = db.Column(db.String(20), default='read')  # read, write
    shared_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    document = db.relationship('Document', backref='shares')
    shared_with = db.relationship('User', foreign_keys=[shared_with_id])
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    @property
    def is_expired(self):
        """Check if share has expired."""
        if self.expiry_date is None:
            return False
        return datetime.utcnow() > self.expiry_date

    def can_access(self, user_id):
        """Check if user can access with this share."""
        return (not self.is_expired and 
                self.shared_with_id == user_id)
    
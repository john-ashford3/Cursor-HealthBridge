from app import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50))  # 'share', 'revoke', 'upload'
    record_id = db.Column(db.Integer, db.ForeignKey('medical_record.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'type': self.type,
            'record_id': self.record_id,
            'created_at': self.created_at.isoformat(),
            'is_read': self.is_read
        } 
from app.models.notification import Notification
from app import db

def create_notification(user_id, message, notification_type, record_id=None):
    notification = Notification(
        user_id=user_id,
        message=message,
        type=notification_type,
        record_id=record_id
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def mark_as_read(notification_id, user_id):
    notification = Notification.query.filter_by(
        id=notification_id, 
        user_id=user_id
    ).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False 
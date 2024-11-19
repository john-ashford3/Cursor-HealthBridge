from flask_mail import Mail, Message
from flask import current_app, render_template_string
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, template, **kwargs):
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=render_template_string(template, **kwargs)
    )
    
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

# Email templates
SHARE_NOTIFICATION_TEMPLATE = """
<h2>New Medical Record Shared</h2>
<p>{{ sender_name }} has shared a medical record with you.</p>
<p>Record Details:</p>
<ul>
    <li>Category: {{ record.category }}</li>
    <li>Date: {{ record.upload_date.strftime('%Y-%m-%d') }}</li>
    <li>Access Level: {{ access_level }}</li>
</ul>
<p>You can view this record by logging into your HealthBridge account.</p>
"""

ACCESS_REVOKED_TEMPLATE = """
<h2>Access Revoked</h2>
<p>{{ sender_name }} has revoked your access to a medical record.</p>
<p>Record Details:</p>
<ul>
    <li>Category: {{ record.category }}</li>
    <li>Date: {{ record.upload_date.strftime('%Y-%m-%d') }}</li>
</ul>
"""

NEW_UPLOAD_NOTIFICATION_TEMPLATE = """
<h2>New Medical Record Upload</h2>
<p>A new medical record has been uploaded for {{ patient_name }}.</p>
<p>Record Details:</p>
<ul>
    <li>Category: {{ record.category }}</li>
    <li>Date: {{ record.upload_date.strftime('%Y-%m-%d') }}</li>
</ul>
<p>You can view this record by logging into your HealthBridge account.</p>
""" 
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.physician import physician
from app.models.user import User, Document, DocumentRequest
from app.physician.forms import DocumentRequestForm, AddPatientForm, DocumentUploadForm
import os
from datetime import datetime

def save_document(form_document, patient_id):
    """Save uploaded document with a secure filename."""
    if form_document:
        # Create a secure filename
        filename = secure_filename(form_document.filename)
        # Add timestamp to filename to make it unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Create the upload directory if it doesn't exist
        upload_dir = os.path.join(current_app.root_path, 'static', 'documents', str(patient_id))
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file
        filepath = os.path.join(upload_dir, filename)
        form_document.save(filepath)
        
        return filename
    return None

@physician.route('/request-document', methods=['POST'])
@login_required
def request_document():
    """Request a document from a patient."""
    if not current_user.is_physician:
        flash('Only physicians can request documents.', 'danger')
        return redirect(url_for('main.home'))
    
    form = DocumentRequestForm()
    if form.validate_on_submit():
        document_request = DocumentRequest(
            document_type=form.document_type.data,
            description=form.description.data,
            due_date=form.due_date.data,
            requesting_physician_id=current_user.id,
            patient_id=form.patient_id.data,
            status='pending'
        )
        db.session.add(document_request)
        db.session.commit()
        flash('Document request sent successfully!', 'success')
    else:
        flash('Error in form submission. Please try again.', 'danger')
    
    return redirect(url_for('main.dashboard'))

@physician.route('/view-patient/<int:patient_id>')
@login_required
def view_patient(patient_id):
    """View patient details and documents."""
    if not current_user.is_physician:
        flash('Only physicians can view patient details.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = User.query.get_or_404(patient_id)
    if patient not in current_user.patients:
        flash('You are not authorized to view this patient\'s details.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    documents = Document.query.filter_by(user_id=patient_id).order_by(Document.uploaded_at.desc()).all()
    document_requests = DocumentRequest.query.filter_by(
        requesting_physician_id=current_user.id,
        patient_id=patient_id
    ).order_by(DocumentRequest.requested_at.desc()).all()
    
    return render_template('physician/view_patient.html',
                         patient=patient,
                         documents=documents,
                         document_requests=document_requests)

@physician.route('/add-patient', methods=['POST'])
@login_required
def add_patient():
    """Add a patient to physician's patient list."""
    if not current_user.is_physician:
        flash('Only physicians can add patients.', 'danger')
        return redirect(url_for('main.home'))
    
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = User.query.filter_by(email=form.email.data).first()
        
        if not patient:
            flash('No patient found with that email address.', 'danger')
            return redirect(url_for('main.dashboard'))
            
        if patient in current_user.patients:
            flash('This patient is already in your patient list.', 'warning')
            return redirect(url_for('main.dashboard'))
            
        current_user.patients.append(patient)
        db.session.commit()
        flash(f'Patient {patient.name} has been added to your patient list.', 'success')
    else:
        flash('Invalid form submission. Please try again.', 'danger')
    
    return redirect(url_for('main.dashboard'))

@physician.route('/upload-document', methods=['POST'])
@login_required
def upload_document():
    """Handle document upload for a patient."""
    if not current_user.is_physician:
        flash('Only physicians can upload documents.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = DocumentUploadForm()
    if form.validate_on_submit():
        patient_id = form.patient_id.data
        
        # Check if patient belongs to physician
        if patient_id not in [p.id for p in current_user.patients]:
            flash('You are not authorized to upload documents for this patient.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        filename = save_document(form.document.data, patient_id)
        if filename:
            document = Document(
                filename=filename,
                original_filename=form.document.data.filename,
                document_type=form.document_type.data,
                description=form.description.data,
                user_id=patient_id,
                uploading_physician_id=current_user.id
            )
            db.session.add(document)
            db.session.commit()
            flash('Document uploaded successfully!', 'success')
        else:
            flash('Error uploading document.', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('main.dashboard'))

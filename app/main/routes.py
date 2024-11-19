from flask import render_template, flash, redirect, url_for, request, current_app, send_from_directory, abort
from flask_login import current_user, login_required
from app import db
from app.main import main  # Import the blueprint
from app.main.forms import (
    ProfileForm, 
    DocumentUploadForm, 
    MedicalQuestionnaireForm,
    AddPatientForm  # Add this import
)
from app.models.user import User, Document, DocumentRequest
from app.main.utils import save_picture  # Add this import
from PIL import Image
import os
import secrets
from werkzeug.utils import secure_filename
from datetime import datetime

@main.route('/')
@main.route('/home')
def home():
    """Home page route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/home.html', title='Home')

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route."""
    if current_user.is_physician:
        # Create forms for modals
        add_patient_form = AddPatientForm()
        upload_form = DocumentUploadForm()
        
        if current_user.physician_type == 'both':
            document_requests = DocumentRequest.query.filter_by(
                requesting_physician_id=current_user.id
            ).order_by(DocumentRequest.requested_at.desc()).all()
            
            recent_uploads = Document.query.filter_by(
                uploading_physician_id=current_user.id
            ).order_by(Document.uploaded_at.desc()).all()
            
            return render_template('physician/combined_dashboard.html',
                                document_requests=document_requests,
                                recent_uploads=recent_uploads,
                                form=add_patient_form,
                                upload_form=upload_form)
        elif current_user.physician_type == 'receiving':
            return render_template('physician/receiving_dashboard.html',
                                form=add_patient_form)
        elif current_user.physician_type == 'sending':
            return render_template('physician/sending_dashboard.html',
                                form=add_patient_form)
    
    # Regular patient dashboard
    documents = Document.query.filter_by(user_id=current_user.id)\
        .order_by(Document.uploaded_at.desc()).all()
    form = DocumentUploadForm()
    return render_template('main/dashboard.html', title='Dashboard', documents=documents, form=form)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # Update user profile with form data
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        current_user.date_of_birth = form.date_of_birth.data
        current_user.address = form.address.data
        
        # Emergency Contact
        current_user.emergency_contact_name = form.emergency_contact_name.data
        current_user.emergency_contact_relationship = form.emergency_contact_relationship.data
        current_user.emergency_contact_phone = form.emergency_contact_phone.data
        
        # Insurance
        current_user.insurance_provider = form.insurance_provider.data
        current_user.insurance_policy_number = form.insurance_policy_number.data
        current_user.insurance_group_number = form.insurance_group_number.data
        
        db.session.commit()
        flash('Your profile has been updated successfully.', 'success')
        return redirect(url_for('main.profile'))
        
    elif request.method == 'GET':
        # Pre-fill form with existing user data
        form.name.data = current_user.name
        form.phone.data = getattr(current_user, 'phone', None)
        form.date_of_birth.data = getattr(current_user, 'date_of_birth', None)
        form.address.data = getattr(current_user, 'address', None)
        
        # Emergency Contact
        form.emergency_contact_name.data = getattr(current_user, 'emergency_contact_name', None)
        form.emergency_contact_relationship.data = getattr(current_user, 'emergency_contact_relationship', None)
        form.emergency_contact_phone.data = getattr(current_user, 'emergency_contact_phone', None)
        
        # Insurance
        form.insurance_provider.data = getattr(current_user, 'insurance_provider', None)
        form.insurance_policy_number.data = getattr(current_user, 'insurance_policy_number', None)
        form.insurance_group_number.data = getattr(current_user, 'insurance_group_number', None)
    
    return render_template('main/profile.html', title='Profile', form=form)

@main.route('/medical-questionnaire', methods=['GET', 'POST'])
@login_required
def medical_questionnaire():
    """Handle medical questionnaire for patients."""
    if current_user.is_physician:
        flash('Physicians cannot fill out medical questionnaires.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    form = MedicalQuestionnaireForm()
    if form.validate_on_submit():
        # Update user medical information
        current_user.medical_history = form.medical_history.data
        current_user.current_medications = form.current_medications.data
        current_user.allergies = form.allergies.data
        current_user.family_history = form.family_history.data
        current_user.lifestyle_info = form.lifestyle_info.data
        current_user.has_completed_questionnaire = True
        
        db.session.commit()
        flash('Medical questionnaire submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    # Pre-fill form if user has already completed it
    elif request.method == 'GET':
        form.medical_history.data = current_user.medical_history
        form.current_medications.data = current_user.current_medications
        form.allergies.data = current_user.allergies
        form.family_history.data = current_user.family_history
        form.lifestyle_info.data = current_user.lifestyle_info
    
    return render_template('main/medical_questionnaire.html', 
                         title='Medical Questionnaire',
                         form=form)

@main.route('/documents')
@login_required
def documents():
    """Display user's documents."""
    if current_user.is_physician:
        # For physicians, show documents they've uploaded
        documents = Document.query.filter_by(
            uploading_physician_id=current_user.id
        ).order_by(Document.uploaded_at.desc()).all()
        
        # Also get their patients' documents
        patient_documents = []
        for patient in current_user.patients:
            patient_docs = Document.query.filter_by(user_id=patient.id).all()
            patient_documents.extend(patient_docs)
            
        return render_template('main/documents.html',
                             title='Documents',
                             uploaded_documents=documents,
                             patient_documents=patient_documents)
    else:
        # For patients, show their documents
        documents = Document.query.filter_by(
            user_id=current_user.id
        ).order_by(Document.uploaded_at.desc()).all()
        
        return render_template('main/documents.html',
                             title='My Documents',
                             documents=documents)

@main.route('/documents/<int:document_id>')
@login_required
def view_document(document_id):
    """View/download a specific document."""
    document = Document.query.get_or_404(document_id)
    
    # Check if user has permission to view this document
    if not (current_user.id == document.user_id or 
            (current_user.is_physician and document.user_id in [p.id for p in current_user.patients]) or
            current_user.is_admin):
        flash('You do not have permission to view this document.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get the document file path
    document_path = os.path.join(
        current_app.root_path, 
        'static', 
        'documents',
        str(document.user_id),
        document.filename
    )
    
    return send_from_directory(
        os.path.dirname(document_path),
        os.path.basename(document_path),
        as_attachment=True,
        download_name=document.original_filename
    )

def save_document(form_document, user_id):
    """Helper function to save uploaded document."""
    if form_document:
        filename = secure_filename(form_document.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        upload_dir = os.path.join(current_app.root_path, 'static', 'documents', str(user_id))
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, filename)
        form_document.save(filepath)
        
        return filename
    return None

@main.route('/upload-document', methods=['POST'])
@login_required
def upload_document():
    """Handle document upload for patients."""
    if current_user.is_physician:
        flash('Physicians should use the physician portal to upload documents.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    form = DocumentUploadForm()
    if form.validate_on_submit():
        filename = save_document(form.document.data, current_user.id)
        if filename:
            document = Document(
                filename=filename,
                original_filename=form.document.data.filename,
                document_type=form.document_type.data,
                description=form.description.data,
                user_id=current_user.id
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

@main.route('/download-document/<int:document_id>')
@login_required
def download_document(document_id):
    """Download a specific document."""
    document = Document.query.get_or_404(document_id)
    
    # Security check: ensure user has permission to download this document
    if not (document.user_id == current_user.id or 
            (current_user.is_physician and document.user_id in [p.id for p in current_user.patients]) or
            current_user.is_admin):
        abort(403)  # Forbidden
    
    # Get document directory path
    document_dir = os.path.join(
        current_app.root_path,
        'static',
        'documents',
        str(document.user_id)
    )
    
    # Check if file exists
    if not os.path.exists(os.path.join(document_dir, document.filename)):
        abort(404)  # Not found
    
    return send_from_directory(
        document_dir,
        document.filename,
        as_attachment=True,
        download_name=document.original_filename
    )

# ... rest of your routes code ... 
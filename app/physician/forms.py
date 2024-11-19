from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class DocumentRequestForm(FlaskForm):
    patient_id = HiddenField('Patient ID', validators=[DataRequired()])
    document_type = SelectField('Document Type', choices=[
        ('medical_report', 'Medical Report'),
        ('lab_result', 'Laboratory Result'),
        ('prescription', 'Prescription'),
        ('imaging', 'Imaging Results'),
        ('vaccination', 'Vaccination Record'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Send Request') 

class PhysicianProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    license_number = StringField('License Number', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Office Address', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Update Profile')

class AddPatientForm(FlaskForm):
    email = StringField('Patient Email', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Add Patient') 

class DocumentUploadForm(FlaskForm):
    patient_id = HiddenField('Patient ID', validators=[DataRequired()])
    document = FileField('Document', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files are allowed!')
    ])
    document_type = SelectField('Document Type', choices=[
        ('medical_report', 'Medical Report'),
        ('lab_result', 'Laboratory Result'),
        ('prescription', 'Prescription'),
        ('imaging', 'Imaging Results'),
        ('vaccination', 'Vaccination Record'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Upload Document') 
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired

class DocumentUploadForm(FlaskForm):
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
        ('insurance', 'Insurance Document'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Upload Document')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    
    # Emergency Contact Information
    emergency_contact_name = StringField('Emergency Contact Name', 
                                       validators=[Optional(), Length(max=120)])
    emergency_contact_relationship = StringField('Relationship to Emergency Contact', 
                                               validators=[Optional(), Length(max=50)])
    emergency_contact_phone = StringField('Emergency Contact Phone', 
                                        validators=[Optional(), Length(max=20)])
    
    # Insurance Information
    insurance_provider = StringField('Insurance Provider', 
                                   validators=[Optional(), Length(max=100)])
    insurance_policy_number = StringField('Policy Number', 
                                        validators=[Optional(), Length(max=50)])
    insurance_group_number = StringField('Group Number', 
                                       validators=[Optional(), Length(max=50)])
    
    submit = SubmitField('Update Profile')

class AddPatientForm(FlaskForm):
    email = EmailField('Patient Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    submit = SubmitField('Add Patient')

class MedicalQuestionnaireForm(FlaskForm):
    medical_history = TextAreaField('Medical History', 
        description='List any past medical conditions, surgeries, or hospitalizations.',
        validators=[DataRequired(), Length(max=2000)])
    
    current_medications = TextAreaField('Current Medications',
        description='List all current medications, including dosage and frequency.',
        validators=[DataRequired(), Length(max=1000)])
    
    allergies = TextAreaField('Allergies',
        description='List any allergies to medications, foods, or other substances.',
        validators=[DataRequired(), Length(max=500)])
    
    family_history = TextAreaField('Family Medical History',
        description='List any significant medical conditions in your immediate family.',
        validators=[DataRequired(), Length(max=1000)])
    
    lifestyle_info = TextAreaField('Lifestyle Information',
        description='Describe your exercise habits, diet, smoking/alcohol use, etc.',
        validators=[DataRequired(), Length(max=1000)])
    
    submit = SubmitField('Submit Questionnaire')

# Add any other forms you need here...
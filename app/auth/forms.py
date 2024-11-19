from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    user_type = SelectField('I am a:', choices=[('patient', 'Patient'), ('physician', 'Healthcare Provider')], validators=[DataRequired()])
    physician_type = SelectField('Provider Type', choices=[('receiving', 'Receiving Provider'), ('sending', 'Sending Provider'), ('both', 'Both - Send and Receive')])
    specialization = StringField('Medical Specialization')
    license_number = StringField('Medical License Number')
    accept_terms = BooleanField('I accept the Terms of Service and Privacy Policy', validators=[DataRequired(message='You must accept the terms to register')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class PhysicianRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    physician_type = RadioField(
        'Physician Type',
        choices=[
            ('receiving', 'Receiving Physician'),
            ('sending', 'Sending Physician'),
            ('both', 'Both - Send and Receive')
        ],
        validators=[DataRequired()]
    )
    specialization = StringField('Medical Specialization', 
        validators=[DataRequired(), Length(max=100)])
    license_number = StringField('Medical License Number', 
        validators=[DataRequired(), Length(max=50)])
    years_of_experience = IntegerField('Years of Experience', 
        validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

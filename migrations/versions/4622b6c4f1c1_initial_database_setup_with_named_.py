"""Initial database setup with named constraints

Revision ID: 4622b6c4f1c1
Revises: 
Create Date: 2024-11-19 07:54:19.249250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4622b6c4f1c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_physician', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('emergency_contact_name', sa.String(length=120), nullable=True),
    sa.Column('emergency_contact_relationship', sa.String(length=50), nullable=True),
    sa.Column('emergency_contact_phone', sa.String(length=20), nullable=True),
    sa.Column('insurance_provider', sa.String(length=100), nullable=True),
    sa.Column('insurance_policy_number', sa.String(length=50), nullable=True),
    sa.Column('insurance_group_number', sa.String(length=50), nullable=True),
    sa.Column('medical_history', sa.Text(), nullable=True),
    sa.Column('current_medications', sa.Text(), nullable=True),
    sa.Column('allergies', sa.Text(), nullable=True),
    sa.Column('family_history', sa.Text(), nullable=True),
    sa.Column('lifestyle_info', sa.Text(), nullable=True),
    sa.Column('has_completed_questionnaire', sa.Boolean(), nullable=True),
    sa.Column('physician_type', sa.String(length=20), nullable=True),
    sa.Column('specialization', sa.String(length=100), nullable=True),
    sa.Column('license_number', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('original_filename', sa.String(length=255), nullable=False),
    sa.Column('document_type', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('uploading_physician_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uploading_physician_id'], ['user.id'], name='fk_document_physician'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_document_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document_request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_type', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('requesting_physician_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], name='fk_document_request_patient'),
    sa.ForeignKeyConstraint(['requesting_physician_id'], ['user.id'], name='fk_document_request_physician'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('physician_patients',
    sa.Column('physician_id', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], name='fk_physician_patients_patient'),
    sa.ForeignKeyConstraint(['physician_id'], ['user.id'], name='fk_physician_patients_physician')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('physician_patients')
    op.drop_table('document_request')
    op.drop_table('document')
    op.drop_table('user')
    # ### end Alembic commands ###

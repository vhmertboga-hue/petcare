"""add animals, files, health tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-07
"""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'files',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('content', sa.LargeBinary(), nullable=True),
        sa.Column('s3_key', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('mimetype', sa.String(), nullable=True),
    )

    op.create_table(
        'animals',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('species', sa.String(), nullable=False),
        sa.Column('breed', sa.String(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('color', sa.String(), nullable=True),
        sa.Column('microchip', sa.String(), nullable=True),
        sa.Column('neutered', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('photo_id', sa.Integer(), sa.ForeignKey('files.id'), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('chronic_conditions', sa.Text(), nullable=True),
        sa.Column('medications', sa.Text(), nullable=True),
        sa.Column('vet_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
    )

    op.create_table(
        'vaccinations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('next_date', sa.Date(), nullable=True),
        sa.Column('veterinarian_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('clinic', sa.String(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'medications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dose', sa.String(), nullable=True),
        sa.Column('frequency', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'vet_visits',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('veterinarian_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('clinic', sa.String(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'lab_tests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('result', sa.Text(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'operations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'disease_histories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
    )

    op.create_table(
        'weight_histories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
    )

    op.create_table(
        'health_documents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('animal_id', sa.Integer(), sa.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False),
        sa.Column('file_id', sa.Integer(), sa.ForeignKey('files.id', ondelete='SET NULL'), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('health_documents')
    op.drop_table('weight_histories')
    op.drop_table('disease_histories')
    op.drop_table('operations')
    op.drop_table('lab_tests')
    op.drop_table('vet_visits')
    op.drop_table('medications')
    op.drop_table('vaccinations')
    op.drop_table('animals')
    op.drop_table('files')

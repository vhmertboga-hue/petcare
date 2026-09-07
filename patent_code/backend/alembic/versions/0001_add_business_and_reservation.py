"""create businesses and reservations tables

Revision ID: 0001_add_business_and_reservation
Revises: 
Create Date: 2026-09-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_add_business_and_reservation'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'businesses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=True, unique=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('logo_file_id', sa.Integer(), sa.ForeignKey('files.id', ondelete='SET NULL'), nullable=True),
        sa.Column('photos', sa.JSON(), nullable=True),
        sa.Column('working_hours', sa.JSON(), nullable=True),
        sa.Column('services', sa.JSON(), nullable=True),
        sa.Column('prices', sa.JSON(), nullable=True),
        sa.Column('commission_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('revenue', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('hotel_id', sa.Integer(), sa.ForeignKey('pet_hotels.id', ondelete='CASCADE'), nullable=False),
        sa.Column('pet_type', sa.String(), nullable=False),
        sa.Column('pet_size', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('guests', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('pickup', sa.Boolean(), nullable=True, server_default=sa.text('0')),
        sa.Column('pickup_fee', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # add pet_hotel_id to files table
    with op.batch_alter_table('files') as batch_op:
        batch_op.add_column(sa.Column('pet_hotel_id', sa.Integer(), sa.ForeignKey('pet_hotels.id', ondelete='CASCADE'), nullable=True))


def downgrade():
    with op.batch_alter_table('files') as batch_op:
        batch_op.drop_column('pet_hotel_id')
    op.drop_table('reservations')
    op.drop_table('businesses')

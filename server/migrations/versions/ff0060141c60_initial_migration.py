"""initial migration

Revision ID: ff0060141c60
Revises: 
Create Date: 2024-11-16 20:40:02.618585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff0060141c60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('gender_enum', sa.Enum('male', 'female', name='gender_enum'), nullable=True),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('is_student', sa.Boolean(), nullable=True),
    sa.Column('will_be_coming', sa.Boolean(), nullable=True),
    sa.Column('is_visitor', sa.Boolean(), nullable=True),
    sa.Column('school', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attendances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emergency_contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('relation', sa.String(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('memberevents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memberevents')
    op.drop_table('emergency_contacts')
    op.drop_table('attendances')
    op.drop_table('members')
    op.drop_table('groups')
    op.drop_table('events')
    op.drop_table('admins')
    # ### end Alembic commands ###

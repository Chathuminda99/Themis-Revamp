"""add azure ad sso

Revision ID: a4699eb2ca37
Revises: c4d5e6f7a8b9
Create Date: 2026-03-20 12:42:59.239808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4699eb2ca37'
down_revision: Union[str, None] = 'c4d5e6f7a8b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the enum type first
    authprovider_enum = sa.Enum('local', 'azure_ad', name='authprovider')
    authprovider_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('users', sa.Column('auth_provider', sa.Enum('local', 'azure_ad', name='authprovider'), server_default='local', nullable=False))
    op.add_column('users', sa.Column('azure_oid', sa.String(length=255), nullable=True))
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.create_index(op.f('ix_users_azure_oid'), 'users', ['azure_oid'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_azure_oid'), table_name='users')
    op.alter_column('users', 'password_hash',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.drop_column('users', 'azure_oid')
    op.drop_column('users', 'auth_provider')
    sa.Enum(name='authprovider').drop(op.get_bind(), checkfirst=True)

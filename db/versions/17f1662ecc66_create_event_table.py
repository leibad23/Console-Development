"""Create Event table

Revision ID: 17f1662ecc66
Revises: 
Create Date: 2025-10-04 22:29:48.348056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17f1662ecc66'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("event" , sa.Column("event_id",sa.UUID , unique=True , nullable=False , primary_key=True) ,sa.Column("user_id",sa.VARCHAR , unique=True , nullable=False ))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("event")
    pass

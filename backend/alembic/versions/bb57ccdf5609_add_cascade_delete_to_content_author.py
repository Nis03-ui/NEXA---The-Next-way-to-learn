"""add cascade delete to content author

Revision ID: bb57ccdf5609
Revises: 40e583467265
Create Date: 2026-10-01 17:06:23.683528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb57ccdf5609'
down_revision: Union[str, Sequence[str], None] = '40e583467265'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

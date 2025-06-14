"""create user tables

Revision ID: ccaece4d8b78
Revises: d6dc4a312e44
Create Date: 2025-04-09 16:15:59.842646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccaece4d8b78'
down_revision: Union[str, None] = 'd6dc4a312e44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

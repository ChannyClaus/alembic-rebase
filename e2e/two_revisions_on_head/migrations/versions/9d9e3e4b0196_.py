"""empty message

Revision ID: 9d9e3e4b0196
Revises: 1673531f822c
Create Date: 2024-10-15 18:51:49.888239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d9e3e4b0196'
down_revision: Union[str, None] = '1673531f822c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

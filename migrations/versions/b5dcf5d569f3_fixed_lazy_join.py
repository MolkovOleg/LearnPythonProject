"""Fixed lazy join

Revision ID: b5dcf5d569f3
Revises: 5a7e93cd2107
Create Date: 2024-04-07 13:32:28.984566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5dcf5d569f3'
down_revision: Union[str, None] = '5a7e93cd2107'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

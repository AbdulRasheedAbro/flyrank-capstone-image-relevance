from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Production deployments should generate/adjust this migration after reviewing
    # the SQLAlchemy models. The capstone's local quick-start also supports create_all.
    pass

def downgrade():
    pass

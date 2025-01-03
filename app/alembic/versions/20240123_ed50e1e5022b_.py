"""empty message

Revision ID: ed50e1e5022b
Revises: 002f3b8ea2e3
Create Date: 2024-01-23 16:55:08.996677

"""
import sqlalchemy as sa
from sqlalchemy import orm, select

from alembic import op
from users.models import User

# revision identifiers, used by Alembic.
revision = "ed50e1e5022b"
down_revision = "002f3b8ea2e3"
branch_labels = None
depends_on = None


def update_phone_numbers():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    users = session.scalars(select(User)).all()
    for index, user in enumerate(users):
        user.phone_number = f"+37529000000{str(index)}"
    session.commit()


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredient",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_ingredient_id"), "ingredient", ["id"], unique=False)
    op.create_table(
        "product_ingredient_association",
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(["ingredient_id"], ["ingredient.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ingredient_id", "product_id", name="idx_unique_ingredient_product"),
    )
    op.create_index(
        op.f("ix_product_ingredient_association_id"), "product_ingredient_association", ["id"], unique=False
    )
    op.alter_column("user", "phone_number", existing_type=sa.VARCHAR(), nullable=False)
    op.create_unique_constraint(None, "user", ["phone_number"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    op.alter_column("user", "phone_number", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_index(op.f("ix_product_ingredient_association_id"), table_name="product_ingredient_association")
    op.drop_table("product_ingredient_association")
    op.drop_index(op.f("ix_ingredient_id"), table_name="ingredient")
    op.drop_table("ingredient")
    # ### end Alembic commands ###

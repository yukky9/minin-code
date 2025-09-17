import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, default="minin-code-user")
    light_theme = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    sections = orm.relationship(
        "Section",
        secondary="user_sections",
        backref="users"
    )

    events = orm.relationship(
        "Event",
        secondary="user_events",
        backref="users"
    )

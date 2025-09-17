import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class UserSection(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_sections'

    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    section_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("sections.id"), primary_key=True)

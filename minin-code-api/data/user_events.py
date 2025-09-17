import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class UserEvent(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_events'

    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("events.id"), primary_key=True)

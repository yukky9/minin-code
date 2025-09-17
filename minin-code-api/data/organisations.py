import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Organisation(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'organisations'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String, default='organisation.jpg')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    cords = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    sections = orm.relationship(
        "Section",
        backref="organisations"
    )

    events = orm.relationship(
        "Event",
        backref="organisations"
    )

    news = orm.relationship(
        "News",
        backref="organisations"
    )

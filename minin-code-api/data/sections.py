import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Section(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'sections'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    organisation_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organisations.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String, default='section.jpg')
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date_stamp = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    schedule = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    availability = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    members_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    members_limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

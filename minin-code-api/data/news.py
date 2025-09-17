import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    organisation_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organisations.id"))
    photo = sqlalchemy.Column(sqlalchemy.String, default='news.jpg')
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

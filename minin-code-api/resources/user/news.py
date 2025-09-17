from flask import send_from_directory
from flask_restful import Resource, abort

from data import db_session
from data.news import News


class UserNewsResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        news = session.query(News).all()
        if not news:
            abort(404, message=f"Новостей не найдено")
        res = []
        for item in news:
            res.append({
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'date':  item.date,
                'photo': item.photo
            })
        return {
            'news': res[::-1]
        }, 200


class NewsPhotoResource(Resource):
    @staticmethod
    def get(news_id):
        session = db_session.create_session()
        news = session.query(News).filter(News.id == news_id).first()
        session.commit()
        return send_from_directory('assets/news', news.photo)

import os
import uuid
from flask import request, g
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename

from auth import authenticate
from misc import allowed_file, allowed_file_size
from data import db_session
from data.news import News


class AdminNewsResource(Resource):
    @staticmethod
    @authenticate
    def get():
        session = db_session.create_session()
        news = session.query().filter(News.organisation_id == g.user_id).all()
        return {
            "news": [new.to_dict(only=('id', 'name')) for new in news]
        }, 200


class AdminNewResource(Resource):
    @staticmethod
    @authenticate
    def get():
        news_id = request.args.get('id')
        session = db_session.create_session()
        news = session.query(News).filter(News.id == news_id, News.organisation_id == g.user_id).first()
        if not news:
            abort(404, message=f"Новость с ID [{news_id}] не найдена")
        res = {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "date": news.date,
        }
        return res, 200

    @staticmethod
    @authenticate
    def post():
        title = request.json['title']
        description = request.json['description']
        if 'file' not in request.files:
            abort(400, message="Нет файла")
        file = request.files['file']
        if file.filename == '':
            abort(400, message="Нет выбранного файла")
        filename = None
        if file and allowed_file(file.filename) and allowed_file_size(file.content_length):
            filename = f'{uuid.uuid4()}.{secure_filename(file.filename).split(".")[1]}'
            file.save(os.path.join('assets/1', filename))
        else:
            abort(400, message="Файл некорректен")
        session = db_session.create_session()
        news = News(
            organisation_id=g.user_id,
            photo=filename,
            title=title,
            description=description,
        )
        session.add(news)
        session.commit()
        return "OK", 200

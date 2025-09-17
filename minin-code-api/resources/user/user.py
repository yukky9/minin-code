from sqlalchemy import desc
from flask import request, send_from_directory
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.user_events import UserEvent
from data.events import Event


class UserResource(Resource):
    @staticmethod
    def post():
        user_id = str(request.json['id'])
        username = request.json['username']
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return "OK", 200
        user = User(
            id=user_id,
            username=username
        )
        session.add(user)
        session.commit()
        return "OK", 200

    @staticmethod
    def get():
        user_id = str(request.args.get('id'))
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        user_event_ids = session.query(UserEvent.event_id).filter(UserEvent.user_id == user_id).all()
        event = None
        if user_event_ids:
            event = (session.query(Event)
                     .filter(Event.id.in_([item[0] for item in user_event_ids])).order_by(desc(Event.date)).first())
        return {
            "light_theme": user.light_theme,
            "event": event.to_dict(only=('id', 'name', 'date')) if event else None
        }, 200


class NearestEventPhotoResource(Resource):
        @staticmethod
        def get(event_id):
            session = db_session.create_session()
            event = session.query(Event).filter(Event.id == event_id).first()
            session.commit()
            return send_from_directory('assets/events', event.photo)

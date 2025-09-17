from flask import request, send_from_directory
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.events import Event
from data.user_events import UserEvent


class UserEventsResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get('id')
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        user_event_ids = session.query(UserEvent.event_id).filter(UserEvent.user_id == user_id).all()
        user_events = session.query(Event).filter(Event.id.in_([item[0] for item in user_event_ids])).all()
        return {
            "user_events": [user_event.to_dict(only=('id', 'name', 'availability')) for user_event in user_events]
        }, 200


class UserEventResource(Resource):
    @staticmethod
    def get():
        user_id = str(request.args.get('user_id'))
        event_id = request.args.get('event_id')
        session = db_session.create_session()
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            abort(404, message=f"Мероприятие с ID [{event_id}] не найдено")
        user_participation = None
        if event.availability:
            user_event = session.query(UserEvent).filter(UserEvent.event_id == event_id,
                                                         UserEvent.user_id == user_id).first()
            user_participation = True if user_event else False
        res = {
            "id": event.id,
            "organisation_id": event.organisation_id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "members_limit": event.members_limit,
            "members_amount": event.members_amount,
            "availability": event.availability,
            "lat": event.cords.split(',')[0],
            "lon": event.cords.split(',')[1],
            "user_participation": user_participation
        }
        return res, 200

    @staticmethod
    def post():
        user_id = str(request.json['user_id'])
        event_id = request.json['event_id']
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            abort(404, message=f"Мероприятие с ID [{event_id}] не найдено")
        user_event = session.query(UserEvent).filter(UserEvent.user_id == user_id, UserEvent.event_id == event_id).first()
        if user_event:
            abort(404, message=f"Пользователь с ID [{user_id}] уже участвует в данном мероприятии")
        if event.availability:
            event.members_amount += 1
            user.rating += 5
            if event.members_amount == event.members_limit:
                event.availability = False
            user_event = UserEvent(
                user_id=user_id,
                event_id=event_id
            )
            session.add(user_event)
            session.commit()
        else:
            abort(404, message=f"Мероприятие с ID [{event_id}] недоступно")
        return "OK", 200

    @staticmethod
    def delete():
        user_id = str(request.args.get('user_id'))
        event_id = request.args.get('event_id')
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            abort(404, message=f"Мероприятие с ID [{event_id}] не найдено")
        user_event = session.query(UserEvent).filter(UserEvent.user_id == user_id,
                                                     UserEvent.event_id == event_id).first()
        if not user_event:
            abort(404, message=f"Пользователь с ID [{user_id}] не состоит в секции с ID [{event_id}]")
        event.members_amount -= 1
        user.rating -= 5
        if not event.availability:
            event.availability = True
        session.delete(user_event)
        session.commit()
        return "OK", 200


class EventPhotoResource(Resource):
    @staticmethod
    def get(event_id):
        session = db_session.create_session()
        event = session.query(Event).filter(Event.id == event_id).first()
        session.commit()
        return send_from_directory('assets/events', event.photo)

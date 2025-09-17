import os
import uuid
from flask import request, g
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename

from auth import authenticate
from misc import allowed_file, allowed_file_size
from data import db_session
from data.events import Event


class AdminEventsResource(Resource):
    @staticmethod
    @authenticate
    def get():
        session = db_session.create_session()
        events = session.query(Event).filter(Event.organisation_id == g.user_id).all()
        return {
            "events": [event.to_dict(only=('id', 'name', 'date')) for event in events]
        }, 200


class AdminEventResource(Resource):
    @staticmethod
    @authenticate
    def get():
        event_id = request.args.get('id')
        session = db_session.create_session()
        event = session.query(Event).filter(Event.id == event_id, Event.organisation_id == g.user_id).first()
        res = {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "date": event.date,
            "members_limit": event.members_limit,
            "members_amount": event.members_amount,
            "availability": event.availability,
            "lat": event.cords.split(',')[0],
            "lon": event.cords.split(',')[1],
        }
        return res, 200

    @staticmethod
    @authenticate
    def post():
        name = request.json['name']
        description = request.json['description']
        date = request.json['date']
        members_limit = request.json['members_limit']
        cords = request.json['cords']
        if 'file' not in request.files:
            abort(400, message="Нет файла")
        file = request.files['file']
        if file.filename == '':
            abort(400, message="Нет выбранного файла")
        filename = None
        if file and allowed_file(file.filename) and allowed_file_size(file.content_length):
            filename = f'{uuid.uuid4()}.{secure_filename(file.filename).split(".")[1]}'
            file.save(os.path.join('assets/events', filename))
        else:
            abort(400, message="File is incorrect")
        session = db_session.create_session()
        event = Event(
            organisation_id=g.user_id,
            photo=filename,
            name=name,
            description=description,
            date=date,
            members_limit=members_limit,
            cords=cords
        )
        session.add(event)
        session.commit()
        return "OK", 200

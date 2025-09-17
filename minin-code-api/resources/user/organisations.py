from flask import request, send_from_directory
from flask_restful import Resource, abort

from data import db_session
from data.organisations import Organisation
from data.events import Event
from data.sections import Section


class UserOrganisationsResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        organisations = session.query(Organisation).all()
        if not organisations:
            abort(404, message=f"Организаций не найдено")
        res = []
        for item in organisations:
            res.append({
                'id': item.id,
                'name': item.name,
                'lat': item.cords.split(',')[0],
                'lon': item.cords.split(',')[1],
            })
        return {
            'organisations': res
        }, 200


class UserOrganisationResource(Resource):
    @staticmethod
    def get():
        organisation_id = request.args.get('id')
        session = db_session.create_session()
        organisation = session.query(Organisation).filter(Organisation.id == organisation_id).first()
        if not organisation:
            abort(404, message=f"Организация с ID [{organisation_id}] не найдена")
        events = session.query(Event).filter(Event.organisation_id == organisation_id).all()
        sections = session.query(Section).filter(Section.organisation_id == organisation_id).all()
        res = {
            'name': organisation.name,
            'description': organisation.description,
            'lat': organisation.cords.split(',')[0],
            'lon': organisation.cords.split(',')[1],
            'events': [item.to_dict(only=('id', 'name', 'description', 'date', 'availability')) for item in events],
            'sections': [item.to_dict(only=('id', 'name', 'description', 'availability'))
                         for item in sections]
        }
        return res, 200


class OrganisationPhotoResource(Resource):
    @staticmethod
    def get(organisation_id):
        session = db_session.create_session()
        organisation = session.query(Organisation).filter(Organisation.id == organisation_id).first()
        session.commit()
        return send_from_directory('assets/organisations', organisation.photo)

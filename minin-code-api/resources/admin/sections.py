import os
import uuid
from flask import request, g
from flask_restful import Resource, abort
from werkzeug.utils import secure_filename

from auth import authenticate
from misc import allowed_file, allowed_file_size
from data import db_session
from data.sections import Section


class AdminSectionsResource(Resource):
    @staticmethod
    @authenticate
    def get():
        session = db_session.create_session()
        sections = session.query(Section).filter(Section.organisation_id == g.user_id).all()
        return {
            "sections": [section.to_dict(only=('id', 'name')) for section in sections]
        }, 200


class AdminSectionResource(Resource):
    @staticmethod
    @authenticate
    def get():
        section_id = request.args.get('id')
        session = db_session.create_session()
        section = session.query(Section).filter(Section.id == section_id, Section.organisation_id == g.user_id).first()
        res = {
            "id": section.id,
            "name": section.name,
            "description": section.description,
            "schedule": section.schedule,
            "members_limit": section.members_limit,
            "members_amount": section.members_amount,
            "availability": section.availability,
        }
        return res, 200

    @staticmethod
    @authenticate
    def post():
        name = request.json['name']
        description = request.json['description']
        members_limit = request.json['members_limit']
        schedule = request.json['schedule']
        if 'file' not in request.files:
            abort(400, message="Нет файла")
        file = request.files['file']
        if file.filename == '':
            abort(400, message="Нет выбранного файла")
        filename = None
        if file and allowed_file(file.filename) and allowed_file_size(file.content_length):
            filename = f'{uuid.uuid4()}.{secure_filename(file.filename).split(".")[1]}'
            file.save(os.path.join('assets/sections', filename))
        else:
            abort(400, message="Файл некорректен")
        session = db_session.create_session()
        section = Section(
            organisation_id=g.user_id,
            photo=filename,
            name=name,
            description=description,
            schedule=schedule,
            members_limit=members_limit,
        )
        session.add(section)
        session.commit()
        return "OK", 200

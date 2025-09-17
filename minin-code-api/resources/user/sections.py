from flask import request, send_from_directory
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.sections import Section
from data.user_sections import UserSection


class UserSectionsResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get('id')
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        user_section_ids = session.query(UserSection.section_id).filter(UserSection.user_id == user_id).all()
        user_sections = session.query(Section).filter(Section.id.in_([item[0] for item in user_section_ids])).all()
        return {
            "user_sections": [user_section.to_dict(only=('id', 'name')) for user_section in user_sections]
        }, 200


class UserSectionResource(Resource):
    @staticmethod
    def get():
        user_id = str(request.args.get('user_id'))
        section_id = request.args.get('section_id')
        session = db_session.create_session()
        section = session.query(Section).filter(Section.id == section_id).first()
        if not section:
            abort(404, message=f"Секция с ID [{section_id}] не найдена")
        user_participation = None
        if section.availability:
            user_section = session.query(UserSection).filter(UserSection.section_id == section_id,
                                                             UserSection.user_id == user_id).first()
            user_participation = True if user_section else False
        res = {
            "id": section.id,
            "organisation_id": section.organisation_id,
            "name": section.name,
            "description": section.description,
            "members_limit": section.members_limit,
            "members_amount": section.members_amount,
            "availability": section.availability,
            "schedule": section.schedule,
            "user_participation": user_participation
        }
        return res, 200

    @staticmethod
    def post():
        user_id = str(request.json['user_id'])
        section_id = request.json['section_id']
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        section = session.query(Section).filter(Section.id == section_id).first()
        if not section:
            abort(404, message=f"Секция с ID [{section_id}] не найдена")
        user_section = session.query(UserSection).filter(UserSection.user_id == user_id,
                                                         UserSection.section_id == section_id).first()
        if user_section:
            abort(404, message=f"Пользователь с ID [{user_id}] уже состоит в данной секции")
        if section.availability:
            section.members_amount += 1
            if section.members_amount == section.members_limit:
                section.availability = False
            user_section = UserSection(
                user_id=user_id,
                section_id=section_id
            )
            session.add(user_section)
            session.commit()
        else:
            abort(404, message=f"Секция с ID [{section_id}] недоступна")
        return "OK", 200

    @staticmethod
    def delete():
        user_id = str(request.args.get('user_id'))
        section_id = request.args.get('section_id')
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        section = session.query(Section).filter(Section.id == section_id).first()
        if not section:
            abort(404, message=f"Секция с ID [{section_id}] не найдена")
        user_section = session.query(UserSection).filter(UserSection.user_id == user_id,
                                                         UserSection.section_id == section_id).first()
        if not user_section:
            abort(404, message=f"Пользователь с ID [{user_id}] не состоит в секции с ID [{section_id}]")
        section.members_amount -= 1
        if not section.availability:
            section.availability = True
        session.delete(user_section)
        session.commit()
        return "OK", 200


class SectionPhotoResource(Resource):
    @staticmethod
    def get(section_id):
        session = db_session.create_session()
        section = session.query(Section).filter(Section.id == section_id).first()
        session.commit()
        return send_from_directory('assets/sections', section.photo)

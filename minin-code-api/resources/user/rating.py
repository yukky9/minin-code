from flask import request
from flask_restful import Resource

from data import db_session
from data.users import User


class RatingResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get('id')
        session = db_session.create_session()
        users = session.query(User).all()
        rating = []
        h = 0
        for user in users:
            h += 1
            if h > 100:
                break
            rating.append({
                'id': user.id,
                'username': user.username,
                'rating': user.rating,
            })
        rating = sorted(rating, key=lambda x: x['rating'], reverse=True)
        user_index = [x for x in range(len(rating)) if rating[x]["id"] == user_id][0]
        user_info = rating[user_index], user_index + 1
        return {
            'rating': rating,
            'user_info': user_info,
        }, 200

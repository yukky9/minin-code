import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
# from flask_ngrok import run_with_ngrok

from resources import *
from data import db_session
from config import RUN_WITH_NGROK, DEBUG, SECRET_KEY, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH
app = Flask(__name__)
CORS(app, supports_credentials=True)

# run_with_ngrok(app) if RUN_WITH_NGROK else None

app.config.update({
    "SECRET_KEY": SECRET_KEY,
    "JSON_AS_ASCII": False,
    "UPLOAD_FOLDER": "assets",
    "MAX_CONTENT_LENGTH": MAX_CONTENT_LENGTH,
    "ALLOWED_EXTENSIONS": ALLOWED_EXTENSIONS,
})


@app.route("/")
def check_work():
    return "OK"


if not os.path.isdir("db"):
    os.mkdir("db")
db_session.global_init("db/MininCode.db")


api = Api(app)
api.add_resource(UserEventsResource, "/user/events")
api.add_resource(UserEventResource, "/user/event")
api.add_resource(EventPhotoResource, "/user/event/<int:event_id>")
api.add_resource(UserNewsResource, "/user/news")
api.add_resource(NewsPhotoResource, "/user/news/<int:news_id>")
api.add_resource(UserOrganisationsResource, "/user/organisations")
api.add_resource(UserOrganisationResource, "/user/organisation")
api.add_resource(OrganisationPhotoResource, "/user/organisation/<int:organisation_id>")
api.add_resource(RatingResource, "/user/rating")
api.add_resource(UserSectionsResource, "/user/sections")
api.add_resource(UserSectionResource, "/user/section")
api.add_resource(SectionPhotoResource, "/user/section/<int:section_id>")
api.add_resource(UserResource, "/user")
api.add_resource(NearestEventPhotoResource, "/user/nearest_event/<int:event_id>")

api.add_resource(AdminSectionsResource, "/admin/sections")
api.add_resource(AdminSectionResource, "/admin/section")
api.add_resource(AdminEventsResource, "/admin/events")
api.add_resource(AdminEventResource, "/admin/event")
api.add_resource(AdminNewsResource, "/admin/news")
api.add_resource(AdminNewResource, "/admin/new")


def main():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()

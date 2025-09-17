import os
# from keycloak import KeycloakOpenID
from dotenv import load_dotenv


load_dotenv()

# development settings
RUN_WITH_NGROK = os.getenv("RUN_WITH_NGROK")
DEBUG = os.getenv("DEBUG")


# flask app settings
SECRET_KEY = os.getenv("SECRET_KEY")


# keycloak settings
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_USER_REALM_NAME = os.getenv("KEYCLOAK_USER_REALM_NAME")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET_KEY = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY")

# keycloak_openid = KeycloakOpenID(
#     server_url=KEYCLOAK_SERVER_URL,
#     client_id=KEYCLOAK_CLIENT_ID,
#     realm_name=KEYCLOAK_USER_REALM_NAME,
#     client_secret_key=KEYCLOAK_CLIENT_SECRET_KEY
# )


# postgresql database settings
DATABASE_URL = os.getenv("DATABASE_URL")


# files settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

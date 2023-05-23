from flask_restx import fields

from extensions import api

register_model = api.model("RegisterModel", {
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
})

login_model = api.model("LoginModel", {
    "email": fields.String,
    "password": fields.String
})

private_user_model = api.model("PrivateUser", {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
})

public_user_model = api.model("PublicUser", {
    "id": fields.Integer,
    "username": fields.String,
})
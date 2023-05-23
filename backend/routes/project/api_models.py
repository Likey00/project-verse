from flask_restx import fields

from extensions import api


project_model = api.model("Project", {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "user_id": fields.Integer
})

project_input_model = api.model("ProjectInput", {
    "title": fields.String,
    "description": fields.String
})
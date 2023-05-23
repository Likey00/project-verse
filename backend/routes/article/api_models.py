from flask_restx import fields

from extensions import api


article_model = api.model("Article", {
    "id": fields.Integer,
    "title": fields.String,
    "text": fields.String,
    "project_id": fields.Integer
})

article_input_model = api.model("ArticleInput", {
    "title": fields.String,
    "text": fields.String
})
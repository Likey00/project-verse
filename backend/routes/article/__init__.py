from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import authorizations
from .db_models import Article
from routes.project.db_models import Project
from routes.user.db_models import User
from .api_models import article_model, article_input_model


ns = Namespace("articles", authorizations=authorizations)


@ns.route("/")
class ArticleListAPI(Resource):
    @ns.marshal_list_with(article_model)
    def get(self):
        return Article.query.all()


@ns.route("/<int:id>")
class ArticleAPI(Resource):
    @ns.marshal_with(article_model)
    def get(self, id):
        return Article.query.get(id)

    @jwt_required()
    @ns.doc(security="jsonWebToken") 
    @ns.expect(article_input_model)
    def put(self, id):
        article = Article.query.get(id)
        if not article:
            return {"error": "Article doesn't exist"}
        project = Project.query.get(article.project_id)
        if project.user_id != get_jwt_identity():
            return {"error": "Not your article"}
        article.update(ns.payload["title"], ns.payload["text"])
        return {"message": "Article updated successfully!"}
    
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    def delete(self, id):
        article = Article.query.get(id)
        if not article:
            return {"error": "Article doesn't exist"}
        project = Project.query.get(article.project_id)
        if project.user_id != get_jwt_identity():
            return {"error": "Not your article"}
        article.delete()
        return {}, 204


@ns.route("/project/<int:id>")
class ArticleProjectAPI(Resource):
    @ns.marshal_list_with(article_model)
    def get(self, id):
        return Project.query.get(id).articles
    
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.expect(article_input_model)
    def post(self, id):
        project = Project.query.get(id)
        if not project:
            return {"error": "Project doesn't exist"}
        if project.user_id != get_jwt_identity():
            return {"error": "Not your project"}
        article = Article(
            title=ns.payload["title"],
            text=ns.payload["text"],
            project=project
        )
        article.add()
        return {"message": "Article added successfully!"}, 201
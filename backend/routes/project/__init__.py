from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import authorizations
from .db_models import Project
from routes.user.db_models import User
from .api_models import project_model, project_input_model


ns = Namespace("projects", authorizations=authorizations)


@ns.route("/")
class ProjectListAPI(Resource):
    @ns.marshal_list_with(project_model)
    def get(self):
        return Project.query.all()
    
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.expect(project_input_model)
    @ns.marshal_with(project_model)
    def post(self):
        project = Project(
            title=ns.payload["title"], 
            description=ns.payload["description"],
            user=User.query.get(get_jwt_identity())
        )
        project.add()
        return project, 201


@ns.route("/<int:id>")
class ProjectAPI(Resource):
    @ns.marshal_with(project_model)
    def get(self, id):
        return Project.query.get(id)
    
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    @ns.expect(project_input_model)
    def put(self, id):
        project = Project.query.get(id)
        if not project:
            return {"error": "Project doesn't exist"}
        if project.user_id != get_jwt_identity():
            return {"error": "Not your project"}
        project.update(ns.payload["title"], ns.payload["description"])
        return {"message": "Project updated successfully!"}
    
    @jwt_required()
    @ns.doc(security="jsonWebToken")
    def delete(self, id):
        project = Project.query.get(id)
        if not project:
            return {"error": "Project doesn't exist"}
        if project.user_id != get_jwt_identity():
            return {"error": "Not your project"}
        project.delete()
        return {}, 204


@ns.route("/user/<int:id>")
class ProjectUserAPI(Resource):
    @ns.marshal_list_with(project_model)
    def get(self, id):
        return User.query.get(id).projects
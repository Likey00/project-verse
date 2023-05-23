from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import authorizations
from .api_models import private_user_model, public_user_model, register_model, login_model
from .db_models import User


ns = Namespace("users", authorizations=authorizations)


@ns.route("/register")
class RegisterAPI(Resource):
    @ns.expect(register_model)
    @ns.marshal_with(private_user_model)
    def post(self):
        user = User(
            username=ns.payload["username"],
            email=ns.payload["email"],
            password_hash=generate_password_hash(ns.payload["password"])
        )
        user.add()
        return user, 201


@ns.route("/login")
class LoginAPI(Resource):
    @ns.expect(login_model)
    def post(self):
        user = User.query.filter_by(email=ns.payload["email"]).first()
        if not user:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(user.password_hash, ns.payload["password"]):
            return {"error": "Incorrect password"}, 401
        return {"access token": create_access_token(identity=user.id)} 


@ns.route("/account")
class AccountAPI(Resource):
    method_decorators = [jwt_required()]

    @ns.doc(security="jsonWebToken")
    @ns.marshal_with(private_user_model)
    def get(self):
        return User.query.get(get_jwt_identity())

    @ns.doc(security="jsonWebToken")
    @ns.expect(register_model)
    @ns.marshal_with(private_user_model)
    def put(self):
        user = User.query.get(get_jwt_identity())
        username, email = ns.payload["username"], ns.payload["email"]
        password_hash = generate_password_hash(ns.payload["password"])
        user.update(username, email, password_hash)
        return user
    
    @ns.doc(security="jsonWebToken")
    def delete(self):
        user = User.query.get(get_jwt_identity())
        user.delete()
        return {}, 204    


@ns.route("/")
class UserListAPI(Resource):
    @ns.marshal_list_with(public_user_model)
    def get(self):
        return User.query.all()
    

@ns.route("/<int:id>")
class UserAPI(Resource):
    @ns.marshal_with(public_user_model)
    def get(self, id):
        return User.query.get(id)

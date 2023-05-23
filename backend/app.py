from flask import Flask
from flask_migrate import Migrate

import routes
from extensions import api, db, jwt


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["JWT_SECRET_KEY"] = "thisisasecret"

api.init_app(app)
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
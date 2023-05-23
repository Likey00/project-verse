from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(320), unique=True)
    password_hash = db.Column(db.String(100))
    projects = db.relationship("Project", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
from extensions import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="projects")
    articles = db.relationship("Article", back_populates="project")

    def __repr__(self):
        return f"<Project {self.title}>"
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

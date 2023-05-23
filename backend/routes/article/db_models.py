from extensions import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="articles")
    
    def __repr__(self):
        return f"<Article {self.title}>"
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, title, text):
        self.title = title
        self.text = text
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
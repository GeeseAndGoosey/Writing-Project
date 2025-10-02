from . import db
from flask_login import UserMixin
from datetime import date

class User (UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable=False) #column to store usernames, maxlength is 150 char and must be unique
    password = db.Column (db.String(150), nullable=False)
    projects = db.relationship("Project", backref = "owner", lazy = True)

    
class Project (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(300))
    content = db.Column(db.Text, default = "")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

class WordCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
    date = db.Column(db.Date, default = date.today)
    words_written = db.Column(db.Integer, default = 0)
    project = db.relationship("Project", backref = "word_counts")
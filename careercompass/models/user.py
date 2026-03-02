from careercompass.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Profile Data
    tech_skills = db.Column(db.String(500), nullable=True) # Comma-separated or JSON
    soft_skills = db.Column(db.String(500), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}')"

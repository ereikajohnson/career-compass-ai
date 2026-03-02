from careercompass.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Profile Data
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    profile_pic = db.Column(db.String(200), nullable=True)
    
    # Social Media
    linkedin = db.Column(db.String(200), nullable=True)
    github = db.Column(db.String(200), nullable=True)
    twitter = db.Column(db.String(200), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    
    tech_skills = db.Column(db.String(500), nullable=True) # Comma-separated or JSON
    soft_skills = db.Column(db.String(500), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}')"

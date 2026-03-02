from careercompass.extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=True)
    tech_skills = db.Column(db.Text, nullable=False) # Comma-separated or JSON
    soft_skills = db.Column(db.Text, nullable=False)
    min_qualification = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    availability = db.Column(db.String(50), nullable=True) # Remote, Full-time, etc.
    salary_package = db.Column(db.String(100), nullable=True) # Range or text

    def __repr__(self):
        return f"Job('{self.title}')"

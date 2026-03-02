from careercompass.extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    tech_skills = db.Column(db.Text, nullable=False) # Comma-separated or JSON
    soft_skills = db.Column(db.Text, nullable=False)
    min_qualification = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Job('{self.title}')"

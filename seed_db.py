import os
from app import create_app
from careercompass.extensions import db
from careercompass.models.job import Job

def seed_database():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if jobs already exist
        if Job.query.count() > 0:
            print("Database already contains data. Skipping seeding.")
            return

        # Sample high-quality jobs for recommendations
        sample_jobs = [
            Job(
                title="Frontend Developer (React)",
                company="TechVision Inc.",
                tech_skills="React, JavaScript, CSS3, HTML5, TypeScript",
                soft_skills="Communication, Problem Solving, Teamwork",
                min_qualification="Bachelor's Degree in CS",
                description="Join our team to build stunning user interfaces with React and modern CSS.",
                industry="Software Development",
                availability="Full-time / Remote",
                salary_package="₹8 - ₹12 LPA"
            ),
            Job(
                title="Python Backend Engineer",
                company="DataFlow Solutions",
                tech_skills="Python, Flask, SQL, Django, AWS",
                soft_skills="Analytical Thinking, Attention to Detail",
                min_qualification="2+ Years Experience",
                description="Design and implement robust backend services using Python and cloud technologies.",
                industry="Data Science",
                availability="Full-time",
                salary_package="₹10 - ₹15 LPA"
            ),
            Job(
                title="Full-Stack Developer",
                company="Innovate Hub",
                tech_skills="Python, React, PostgreSQL, Docker, AWS",
                soft_skills="Multi-tasking, Client Management",
                min_qualification="Bachelor's Degree",
                description="Experience building end-to-end applications from database design to UI implementation.",
                industry="Web Services",
                availability="Hybrid",
                salary_package="₹12 - ₹18 LPA"
            ),
            Job(
                title="Machine Learning Engineer",
                company="AI Core Labs",
                tech_skills="Python, Machine Learning, Scikit-learn, NumPy, Pandas",
                soft_skills="Curiosity, Critical Thinking",
                min_qualification="Master's or PhD in AI/ML",
                description="Apply advanced algorithms to solve complex business problems using AI.",
                industry="Artificial Intelligence",
                availability="Full-time / Bangalore",
                salary_package="₹15 - ₹25 LPA"
            ),
            Job(
                title="Data Scientist",
                company="Insight Analytics",
                tech_skills="Python, SQL, Tableau, Statistics, Pandas",
                soft_skills="Storytelling, Business Acumen",
                min_qualification="Bachelor's in Math or Stats",
                description="Extract meaningful insights from large datasets and present them to stakeholders.",
                industry="Analytics",
                availability="Contract",
                salary_package="₹9 - ₹14 LPA"
            ),
            Job(
                title="Cloud Infrastructure Engineer",
                company="SkyScale Cloud",
                tech_skills="AWS, Docker, Kubernetes, Terraform, Linux",
                soft_skills="Incident Management, Adaptability",
                min_qualification="Cloud Certification (AWS/Azure)",
                description="Manage and scale our cloud infrastructure using modern DevOps tools.",
                industry="Cloud Computing",
                availability="Full-time / Remote",
                salary_package="₹14 - ₹20 LPA"
            )
        ]

        # Add to database
        for job in sample_jobs:
            db.session.add(job)
        
        try:
            db.session.commit()
            print("Successfully seeded the database with 6 sample jobs!")
        except Exception as e:
            db.session.rollback()
            print(f"Error while seeding database: {e}")

if __name__ == "__main__":
    seed_database()

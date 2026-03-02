import os
from flask import Flask
from careercompass.extensions import db, login_manager, bcrypt


def create_app(test_config=None):
    app = Flask(__name__, template_folder='careercompass/templates', static_folder='careercompass/static')

    # App Configuration
    app.config['SECRET_KEY'] = 'dev_secret_key_careercompass'
    
    # Support Cloud Databases (Postgres) on Vercel, fallback to local SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'database.db')
    
    # Vercel adds multiple possible variables depending on the integration type
    database_url = (
        os.environ.get('POSTGRES_URL') or 
        os.environ.get('POSTGRES_URL_NON_POOLING') or 
        os.environ.get('DATABASE_URL') or
        os.environ.get('SUPABASE_POSTGRES_URL')
    )
    
    if database_url:
        # Flask-SQLAlchemy requires postgresql:// instead of postgres://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['DB_TYPE'] = 'postgresql'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['DB_TYPE'] = 'sqlite'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    from careercompass.routes.auth_routes import auth_bp
    from careercompass.routes import main_bp
    from careercompass.routes.admin_routes import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # User Loader
    @login_manager.user_loader
    def load_user(user_id):
        from careercompass.models.user import User
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_db_status():
        is_vercel = os.environ.get('VERCEL') == '1'
        db_type = app.config.get('DB_TYPE')
        return dict(is_vercel=is_vercel, db_type=db_type)

    with app.app_context():
        try:
            db.create_all()
            
            # Automatically seed if Cloud DB is empty
            from careercompass.models.job import Job
            if Job.query.count() == 0:
                print("Seeding database...")
                sample_jobs = [
                    Job(title="React Frontend Developer", company="TechVision", tech_skills="React, JavaScript, CSS", soft_skills="Teamwork", min_qualification="Bachelor's", description="Build UI.", industry="Software", availability="Remote", salary_package="₹8 - ₹12 LPA"),
                    Job(title="Python Analyst", company="DataFlow", tech_skills="Python, SQL, Pandas", soft_skills="Logic", min_qualification="Analytical", description="Data insights.", industry="Data", availability="Full-time", salary_package="₹7 - ₹11 LPA"),
                    Job(title="Full Stack Cloud Dev", company="Innovate", tech_skills="Python, React, AWS", soft_skills="Multi-tasking", min_qualification="Dev experience", description="End-to-end dev.", industry="Web", availability="Hybrid", salary_package="₹12 - ₹18 LPA")
                ]
                db.session.add_all(sample_jobs)
                db.session.commit()
                print("Seeded successfully.")
        except Exception as e:
            print(f"DATABASE ERROR during create_all/seeding: {e}")
            # We don't crash the app here, just log it.

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

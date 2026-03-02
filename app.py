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
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Flask-SQLAlchemy requires postgresql:// instead of postgres://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        
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

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database setup skipped or failed: {e}")

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

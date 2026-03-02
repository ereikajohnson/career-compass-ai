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
    
    # Vercel adds POSTGRES_URL or DATABASE_URL depending on the provider
    database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
    
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
        except Exception as e:
            print(f"DATABASE ERROR during create_all: {e}")
            # We don't crash the app here, just log it.

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

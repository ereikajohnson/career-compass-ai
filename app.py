import os
from flask import Flask
from careercompass.extensions import db, login_manager, bcrypt
from careercompass.models.user import User
from careercompass.routes.auth_routes import auth_bp
from careercompass.routes.main_routes import main_bp
from careercompass.routes.admin_routes import admin_bp


def create_app(test_config=None):
    app = Flask(__name__, template_folder='careercompass/templates', static_folder='careercompass/static')

    # App Configuration
    app.config['SECRET_KEY'] = 'dev_secret_key_careercompass'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)   # ← Removed url_prefix='/'
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # User Loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

from flask import Flask, jsonify
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from db import db_retrieve_user

    @login_manager.user_loader
    def load_user(user_id):
        return db_retrieve_user(user_id)

    # blueprint for users routes
    from users import users as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    # blueprint for tasks routes
    from tasks import tasks as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # blueprint for tasks routes
    from comments import comments as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comments')

    # blueprint for auth routes
    from auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='')

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

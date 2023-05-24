from flask import Flask


def create_app():
    app = Flask(__name__)

    # blueprint for users routes
    from users import users as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    # blueprint for tasks routes
    from tasks import tasks as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # blueprint for tasks routes
    from comments import comments as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comments')

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

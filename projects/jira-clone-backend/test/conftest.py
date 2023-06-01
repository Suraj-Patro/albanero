from __init__ import create_app
import pytest
import json


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def user_id(client):
    response = client.post('/users/create', data=json.dumps({
            "userName": "username 1",
            "password": "",
            "name": "name 1",
            "email": "email 1"
        })
    )
    return response.json["data"]["id"] if response.json else ""


@pytest.fixture()
def task_id(client, user_id):
    response = client.post('/tasks/create', data=json.dumps({
            "title": "title 1",
            "description": "desc 1",
            "reporter": user_id,
            "assignee": user_id
        })
    )
    return response.json["data"]["id"] if response.json else ""


@pytest.fixture()
def comment_id(client, user_id, task_id):
    response = client.post('/comments/create', data=json.dumps({
            "message": "message 1",
            "task": task_id,
            "user": user_id
        })
    )
    return response.json["data"]["id"] if response.json else ""

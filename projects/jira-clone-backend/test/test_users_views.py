import json


def test_users_list(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/users/')
    assert response.status_code == 200


def test_users_tasks(client, user_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert user_id != ""
    response = client.get(f'/users/tasks?id={user_id}')
    assert response.status_code == 200


def test_user_create(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/users/create', data=json.dumps({
                "userName": "username 1",
                "password": "",
                "name": "name 1",
                "email": "email 1"
            })
        )
    assert response.status_code == 200


def test_user_retrieve(client, user_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert user_id != ""
    response = client.get(f'/users/retrieve?id={user_id}')
    assert response.status_code == 200


def test_user_update(client, user_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert user_id != ""
    response = client.get(f'/users/update?id={user_id}', data=json.dumps({
                "userName": "username 1",
                "password": "",
                "name": "name 1",
                "email": "email 1"
            })
        )
    assert response.status_code == 200


def test_user_delete(client, user_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert user_id != ""
    response = client.delete(f'/users/delete?id={user_id}')
    assert response.status_code == 200

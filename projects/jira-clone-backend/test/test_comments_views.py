import json


def test_comments_list(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/comments/')
    assert response.status_code == 200



def test_comments_create(client, user_id, task_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments/create' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.post('/comments/create', data=json.dumps({
            "message": "message 1",
            "task": task_id,
            "user": user_id
        })
    )
    assert response.status_code == 200


def test_comments_retrieve(client, comment_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert comment_id != ""
    response = client.get(f'/comments/retrieve?id={comment_id}')
    assert response.status_code == 200


def test_comments_update(client, user_id, task_id, comment_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert comment_id != ""
    response = client.post(f'/comments/update?id={comment_id}', data=json.dumps({
            "message": "message 1",
            "task": task_id,
            "user": user_id
            })
        )
    assert response.status_code == 200


def test_comments_delete(client, comment_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert comment_id != ""
    response = client.delete(f'/users/delete?id={comment_id}')
    assert response.status_code == 200

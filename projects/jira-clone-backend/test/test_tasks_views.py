import json


def test_tasks_list(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/tasks/')
    assert response.status_code == 200


def test_tasks_comments(client, task_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/comments' page is requested (GET)
    THEN check that the response is valid
    """
    assert task_id != ""
    response = client.get(f'/tasks/comments?id={task_id}')
    assert response.status_code == 200


def test_task_create(client, user_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/create' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.post('/tasks/create', data=json.dumps({
            "title": "title 1",
            "description": "desc 1",
            "reporter": user_id,
            "assignee": user_id
        })
    )
    assert response.status_code == 200


def test_task_retrieve(client, task_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert task_id != ""
    response = client.get(f'/users/retrieve?id={task_id}')
    assert response.status_code == 200


def test_task_update(client, user_id, task_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert task_id != ""
    response = client.post(f'/users/update?id={task_id}', data=json.dumps({
                "title": "title 1",
                "description": "desc 1",
                "reporter": user_id,
                "assignee": user_id
            })
        )
    assert response.status_code == 200


def test_task_delete(client, task_id):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/tasks/' page is requested (GET)
    THEN check that the response is valid
    """
    assert task_id != ""
    response = client.delete(f'/users/delete?id={task_id}')
    assert response.status_code == 200

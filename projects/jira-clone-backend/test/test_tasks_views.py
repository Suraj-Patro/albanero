

def test_tasks_list(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/tasks')
    assert response.status_code == 200


def test_tasks_comments(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tasks/comments' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/tasks/comments')
    assert response.status_code == 200

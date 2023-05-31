

def test_users_list(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/users')
    assert response.status_code == 200


def test_users_tasks(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users/tasks' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/users/tasks')
    assert response.status_code == 200

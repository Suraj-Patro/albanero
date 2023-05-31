

def test_comments_list(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/comments' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/comments')
    assert response.status_code == 200

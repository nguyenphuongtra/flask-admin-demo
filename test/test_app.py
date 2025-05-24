from app import app

def test_test_page():
    client = app.test_client()
    response = client.get('/test')
    assert response.status_code == 200
    assert b"This is a test page!" in response.data

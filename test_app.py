import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Chào mừng đến với ứng dụng Flask" in response.data.decode('utf-8')

def test_test_page(client):
    response = client.get('/test')
    assert response.status_code == 200
    assert "Trang kiểm thử!" in response.data.decode('utf-8')

def test_admin_page_access(client):
    response = client.get('/admin/', follow_redirects=True)  # Thêm dấu / và follow_redirects
    assert response.status_code == 200
    assert "Admin Panel" in response.data.decode('utf-8')

def test_admin_add_user(client):
    response = client.post('/admin/user/new/', data={  # Sửa URL thành /admin/user/new/
        'username': 'testuser',
        'email': 'test@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@example.com'
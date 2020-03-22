import pytest
from scrawl import create_app

@pytest.fixture
def client(request):
    app = create_app('flask_test.cfg')
    test_client = app.test_client()
    yield test_client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_db_have_one_test_page(client):
    response = client.get('/pages')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert 'sample page name' in response.json[0]["page_name"]

# def test_create_page(client):

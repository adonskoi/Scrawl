import os
import time
import json
import pytest
from scrawl import create_app, db

@pytest.fixture
def client(request):
    app = create_app('flask_test.cfg')
    test_client = app.test_client()
    yield test_client
    os.remove(app.config.get('DB'))
    

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_db_have_one_test_page(client):
    response = client.get('/api/pages')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert 'sample page name' in response.json[0]["page_name"]

def test_create_page(client):
    data = {"page_name": "first page", "pid": 0}
    response = client.post('/api/pages', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json['_id']

def test_create_page_return_500_without_id_or_name(client):
    data = {"page_name": "first page"}
    response = client.post('/api/pages', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 500
    assert response.json["error"]['message'] == "wrong pid or/and page name"
    data = {"pid": 0}
    response = client.post('/api/pages', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 500

def test_update_page(client):
    data = {"page_name": "first page", "content": {"insert": "some text"}}
    response = client.patch("/api/pages/2", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200

def test_update_return_404_on_non_existing_page(client):
    data = {"page_name": "first page", "content": {"insert": "some text"}}
    response = client.patch("/api/pages/33")
    assert response.status_code == 404

def test_delete_page(client):
    response = client.delete('/api/pages/2')
    assert response.status_code == 200

def test_return_404_on_delete_non_existing_page(client):
    response = client.delete("/api/pages/2")
    assert response.status_code == 404

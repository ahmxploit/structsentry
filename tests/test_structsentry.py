from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_scan_invalid_json():
    r = client.post('/scan', data={'text': '{invalid: json}'})
    assert r.status_code == 200

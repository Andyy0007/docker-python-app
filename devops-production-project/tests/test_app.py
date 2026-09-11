import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from app import app

def test_health():
    r = app.test_client().get('/health')
    assert r.status_code == 200
    assert r.json['status'] == 'UP'

def test_metrics():
    r = app.test_client().get('/metrics')
    assert r.status_code == 200
    assert b'flask_http_requests_total' in r.data

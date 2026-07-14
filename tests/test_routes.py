from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/").status_code == 200

def test_analyze():
    r = client.post("/api/analyze-event", json={"event_description": "AI conference"})
    assert r.status_code == 200
    assert "themes" in r.json()

def test_generate():
    r = client.post("/api/generate-conversation", json={
        "event_description": "Tech meetup",
        "interests": ["AI", "coding"]
    })
    assert r.status_code == 200
    assert "suggestions" in r.json()

def test_invalid():
    assert client.post("/api/generate-conversation", json={}).status_code == 422
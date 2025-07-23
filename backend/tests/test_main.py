import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from backend.main import app

client = TestClient(app)

def test_create_list_update_delete_bot():
    # Vytvoření bota
    resp = client.post("/bots/", json={"name": "TestBot", "description": "Testovací bot"})
    assert resp.status_code == 201
    bot = resp.json()
    bot_id = bot["id"]

    # Načtení seznamu botů
    resp = client.get("/bots/")
    assert resp.status_code == 200
    bots = resp.json()
    assert any(b["id"] == bot_id for b in bots)

    # Detail bota
    resp = client.get(f"/bots/{bot_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "TestBot"

    # Úprava bota
    resp = client.put(f"/bots/{bot_id}", json={"name": "TestBot2", "description": "Upravený"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "TestBot2"

    # Spuštění bota
    resp = client.post(f"/bots/{bot_id}/start")
    assert resp.status_code == 200
    assert resp.json()["status"] == "running"

    # Pozastavení bota
    resp = client.post(f"/bots/{bot_id}/pause")
    assert resp.status_code == 200
    assert resp.json()["status"] == "paused"

    # Manuální obchodování
    resp = client.post(f"/bots/{bot_id}/manual_trade")
    assert resp.status_code == 200
    assert resp.json()["trade"] == "executed"

    # Smazání bota
    resp = client.delete(f"/bots/{bot_id}")
    assert resp.status_code == 204

    # Ověření smazání
    resp = client.get(f"/bots/{bot_id}")
    assert resp.status_code == 404

def test_websocket_realtime():
    with client.websocket_connect("/ws/realtime") as websocket:
        for _ in range(3):
            data = websocket.receive_json()
            assert "price" in data and "volume" in data and "timestamp" in data

def test_failed_trade():
    # Try manual trade on non-existent bot
    resp = client.post("/bots/9999/manual_trade")
    assert resp.status_code == 404

def test_invalid_bot_create():
    # Missing required fields
    resp = client.post("/bots/", json={})
    assert resp.status_code == 422

def test_permission_error():
    # Simulate permission error (assuming /admin endpoint requires auth)
    resp = client.get("/admin/")
    assert resp.status_code in (401, 403)

def test_login_logout_flow():
    # Try login with invalid credentials
    resp = client.post("/auth/login", data={"username": "bad", "password": "wrong"})
    assert resp.status_code == 401

    # Try login with valid credentials (assuming test user exists)
    resp = client.post("/auth/login", data={"username": "test", "password": "test"})
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        assert token
        # Logout
        resp2 = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
        assert resp2.status_code == 200
    else:
        assert resp.status_code == 401

def test_edge_case_bot_update():
    # Update bot with invalid data
    resp = client.post("/bots/", json={"name": "EdgeBot", "description": "Edge"})
    assert resp.status_code == 201
    bot_id = resp.json()["id"]
    resp = client.put(f"/bots/{bot_id}", json={"name": "", "description": ""})
    assert resp.status_code == 422
    client.delete(f"/bots/{bot_id}")
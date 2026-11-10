import os
import uuid

# Must happen before app.core.config.get_settings() is first called.
TEST_DB = f"acm_test_{uuid.uuid4().hex[:8]}"
os.environ["mongodb_database"] = TEST_DB

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from pymongo import MongoClient  # noqa: E402

from app.core.config import get_settings  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
    MongoClient(get_settings().mongodb_url).drop_database(TEST_DB)


def register_and_login(client, email, role, name="Test"):
    pw = "password123"
    r = client.post(
        "/auth/register", json={"email": email, "name": name, "password": pw, "role": role}
    )
    assert r.status_code == 201, r.text
    r = client.post("/auth/login", data={"username": email, "password": pw})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

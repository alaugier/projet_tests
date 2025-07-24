import sys
import os
import numpy as np
# Rajout du dossier parent de ./tests dans le PYTHONPATH pour atteindre le fichier app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_get_index(client):
    response = client.get("/api/data")
    data = response.json # Data est un dictionnaire
    assert data.get("status") == "success"


def test_check_a():
    from app import a
    assert isinstance(a, np.ndarray)
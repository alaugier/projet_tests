import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app

# ---------------------------------------------------
# 🎯 Fixture client Flask pour simuler les requêtes HTTP
# ---------------------------------------------------
@pytest.fixture
def client():
    flask_app.config["TESTING"] = True  # Mode test désactive les erreurs HTML et active un contexte spécial
    with flask_app.test_client() as client:
        yield client  # On renvoie le client pour les tests HTTP
        

# ---------------------------------------------------
# ✅ Test de la route POST /save avec mock MongoDB
# ---------------------------------------------------
@patch("app.MongoClient")  # Remplace app.MongoClient par un mock pendant ce test
def test_save_route_inserts_data(mock_mongo_client, client):
    """
    Ce test simule une insertion MongoDB via la route POST /save
    sans toucher à la vraie base de données MongoDB Atlas.
    """

    # 🧪 1. Création d’un mock de collection MongoDB
    mock_collection = MagicMock()
    mock_collection.insert_one.return_value.acknowledged = True  # Simule un insert réussi

    # 🧪 2. Mock de la base contenant cette collection
    mock_db = MagicMock()
    mock_db.predictions = mock_collection  # On veut accéder à db.predictions

    # 🧪 3. Configuration de MongoClient simulé : client["nlp_classification"] → mock_db
    mock_mongo_client.return_value.__getitem__.return_value = mock_db

    # 🧾 4. Simulation d’un formulaire envoyé en POST
    test_data = {
        "phrase": "Ceci est une phrase testée automatiquement.",
        "prediction": "1",
        "proba": "0.92",
        "correct": "true"
    }

    # 🚀 5. Envoi de la requête POST vers la route /save
    response = client.post("/save", data=test_data)

    # ✅ 6. Vérifications
    assert response.status_code == 200  # La requête doit réussir
    assert b"Donn\xc3\xa9es enregistr\xc3\xa9es avec succ\xc3\xa8s" in response.data  # Le texte de succès apparaît

    # 🔍 7. Vérifie qu’un insert a bien été déclenché
    mock_collection.insert_one.assert_called_once()

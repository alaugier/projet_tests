import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app

# ---------------------------------------------------
# 🎯 Fixture client Flask pour simuler les requêtes HTTP
# ---------------------------------------------------
@pytest.fixture
def client():
    flask_app.config["TESTING"] = True  # Mode test : désactive gestion d'erreurs HTML, active contexte test spécial
    with flask_app.test_client() as client:
        yield client  # On renvoie le client Flask pour les tests HTTP


# ---------------------------------------------------
# ✅ Test de la route POST /save avec mock MongoDB
# ---------------------------------------------------
@patch("app.MongoClient")  # On remplace MongoClient importé dans app.py par un mock pendant ce test
def test_save_route_inserts_data(mock_mongo_client, client):
    """
    Ce test simule une insertion MongoDB via la route POST /save
    sans toucher à la vraie base MongoDB Atlas.

    Le patch remplace MongoClient par un mock.
    On configure la chaîne d'appels : client -> db 'nlp_classification' -> collection 'predictions' -> insert_one.
    """

    # 🧪 1. Création d’un mock pour la méthode insert_one
    mock_insert_one = MagicMock()
    mock_insert_one.return_value.acknowledged = True  # Simule un insert réussi retournant acknowledged=True

    # 🧪 2. Mock de la collection MongoDB 'predictions'
    mock_predictions = MagicMock()
    mock_predictions.insert_one = mock_insert_one

    # 🧪 3. Mock de la base MongoDB 'nlp_classification' qui contient la collection 'predictions'
    mock_db = MagicMock()
    mock_db.predictions = mock_predictions

    # 🧪 4. Configuration du mock MongoClient pour retourner la base mockée
    # Ici, client.nlp_classification doit renvoyer mock_db
    mock_mongo_client.return_value.nlp_classification = mock_db

    # 🧾 5. Données du formulaire simulées envoyées en POST
    test_data = {
        "phrase": "Ceci est une phrase testée automatiquement.",
        "prediction": "1",
        "proba": "0.92",
        "correct": "true"
    }

    # 🚀 6. Envoi de la requête POST vers la route /save avec les données simulées
    response = client.post("/save", data=test_data)

    # ✅ 7. Vérification que la requête a réussi
    assert response.status_code == 200  # Code HTTP 200 OK attendu
    assert b"Donn\xc3\xa9es enregistr\xc3\xa9es avec succ\xc3\xa8s" in response.data  # Message succès dans la réponse

    # 🔍 8. Vérifie que insert_one a bien été appelé une fois sur la collection mockée
    mock_insert_one.assert_called_once()

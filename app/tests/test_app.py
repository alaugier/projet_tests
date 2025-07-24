import sys
import os

# Rajout du dossier parent de ./tests dans le PYTHONPATH pour atteindre app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app, vectorizer, model  # À faire après avoir modifié sys.path

import numpy as np
import pytest

from sklearn.linear_model import LogisticRegression

@pytest.fixture
def client():
    """
    Fixture Pytest pour créer un client de test Flask.
    """
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_get_index(client):
    """
    Teste que la page d'accueil de l'application Flask est accessible et renvoie un code 200.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Analyse de Sentiment</title>" in response.data # Vérifiez un élément du titre HTML


def test_vectorizer_output_shape_and_model_input_compatibility():
    """
    Teste que la forme de sortie du vectorizer est compatible avec la forme d'entrée attendue par le modèle.
    """
    assert vectorizer is not None, "Le vectorizer n'a pas été chargé."
    assert model is not None, "Le modèle n'a pas été chargé."

    test_phrase = ["Ceci est une phrase de test pour la compatibilité."]
    transformed_phrase = vectorizer.transform(test_phrase)

    try:
        model.predict_proba(transformed_phrase)
        print(f"La forme de sortie du vectorizer ({transformed_phrase.shape}) est compatible avec le modèle.")
    except Exception as e:
        pytest.fail(f"La forme de sortie du vectorizer est incompatible avec le modèle: {e}")

    if hasattr(model, 'n_features_in_'):
        assert transformed_phrase.shape[1] == model.n_features_in_, \
            f"Le nombre de features du vectorizer ({transformed_phrase.shape[1]}) ne correspond pas à celui du modèle ({model.n_features_in_})."


def test_prediction_probabilities_range():
    """
    Teste que les probabilités de prédiction retournées par le modèle sont comprises entre 0 et 1.
    """
    assert vectorizer is not None, "Le vectorizer n'a pas été chargé."
    assert model is not None, "Le modèle n'a pas été chargé."

    test_phrase = ["J'adore ce produit, il est génial !"] # Une phrase de test
    
    # Transformer la phrase
    transformed_phrase = vectorizer.transform(test_phrase)
    
    # Obtenir les probabilités
    probabilities = model.predict_proba(transformed_phrase)
    
    # Vérifier que les probabilités sont un tableau NumPy
    assert isinstance(probabilities, np.ndarray), "Les probabilités ne sont pas un tableau NumPy."
    
    # Vérifier que toutes les probabilités sont >= 0
    assert np.all(probabilities >= 0), "Certaines probabilités sont inférieures à 0."
    
    # Vérifier que toutes les probabilités sont <= 1
    assert np.all(probabilities <= 1), "Certaines probabilités sont supérieures à 1."
    
    # Optionnel mais recommandé : vérifier que la somme des probabilités pour chaque échantillon est proche de 1
    # Utiliser np.isclose pour les comparaisons en virgule flottante
    assert np.all(np.isclose(np.sum(probabilities, axis=1), 1.0)), "La somme des probabilités n'est pas proche de 1."

def test_model_is_logistic_regression():
    """
    Teste que le modèle chargé est bien une instance de LogisticRegression.
    """
    assert model is not None, "Le modèle n'a pas été chargé."
    assert isinstance(model, LogisticRegression), "Le modèle n'est pas une instance de LogisticRegression."
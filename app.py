from flask import Flask
from flask import render_template, request, url_for, jsonify, redirect
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import os
from dotenv import load_dotenv

from joblib import load

load_dotenv()

HOST_MONGODB = os.getenv("HOST_MONGODB")
MONGO_DB_APPNAME = os.getenv("MONGO_DB_APPNAME")
PASSWORD_MONGODB = os.getenv("PASSWORD_MONGODB")
USER_MONGODB = os.getenv("USER_MONGODB")

app = Flask(__name__)

try:
    model = load("models/model_logreg.joblib")
except Exception as e:
    print(f"Erreur de chargement du modèle : {e}")

try:
    vectorizer = load("models/tfidf_vectorizer.joblib")
except Exception as e:
    print(f"Erreur de chargement du vectorizer : {e}")

classes = model.classes_


# Page d'accueil
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Page d'accueil de l'application Flask.
    Affiche un formulaire pour saisir une phrase à analyser.
    Si une phrase est soumise via POST, elle est transformée et analysée par le modèle de classification.
    Les résultats de la prédiction sont affichés sur une page de résultat.

    :Methods:
        - GET: Affiche le formulaire de saisie de phrase.
        - POST: Traite la phrase soumise, effectue la transformation et la prédiction
        et redirige vers la page de résultat avec les informations de prédiction.

    :Returns:
        - Template HTML de la page d'accueil avec le formulaire.
        - Template HTML de la page de résultat avec les informations de prédiction si une phrase est soumise.
    
    """

    if request.method == "POST":

        phrase = request.form.get("phrase")

        if phrase:
            # Transformation de la phrase avec le vectorizer
            transformed_phrase = vectorizer.transform([phrase])

            # Prédiction avec le modèle
            probabilities = model.predict_proba(transformed_phrase)[0]
            prediction = classes[np.argmax(probabilities)]
            best_proba = probabilities[np.argmax(probabilities)]
            best_proba = round(best_proba, 2)
            best_proba_human_readable = int(best_proba * 100)

            # Redirection vers la page de résultat
            return render_template("result.html", phrase=phrase, prediction=prediction, proba=best_proba, best_proba_human_readable=best_proba_human_readable)
        
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    """
    Enregistre les données de feedback dans la base de données MongoDB.
    Extrait les informations de la requête POST et les insère dans la collection 'predictions'.
    Redirige vers la page d'accueil après l'enregistrement.
    Assure la connexion à MongoDB avec les informations d'identification stockées dans les variables d'environnement.
    Si une erreur de connexion se produit, renvoie un message d'erreur.

    :Args:
        - phrase (str): La phrase analysée.
        - prediction (int): La prédiction du modèle.
        - best_proba (float): La probabilité associée à la prédiction.
        - correct (bool): Indique si la prédiction est correcte ou non.
    :Returns:
        - Redirection vers la page d'accueil.
    """

    now = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")

    phrase = request.form.get("phrase") #La phrase analysée.
    prediction = int(request.form.get("prediction")) # La prédiction du modèle.
    best_proba = float(request.form.get("proba")) # La probabilité associée à la prédiction.
    correct = request.form.get("correct", False) == "true" # Indique si la prédiction est correcte ou non.

    # Connexion à MongoDB
    uri = f"mongodb+srv://{USER_MONGODB}:{PASSWORD_MONGODB}@{HOST_MONGODB}/?retryWrites=true&w=majority&appName={MONGO_DB_APPNAME}"
    try:
        client = MongoClient(uri, server_api=ServerApi('1')) # On créé un client MongoDB
        db = client.nlp_classification # On se connecte à la base de données
        predictions = db.predictions # On se connecte à la collection 'predictions'
    except Exception as e:
        return render_template("submission.html", message=f"Erreur de connexion à la base de données : {e}") 
    

    feedback_data = {"phrase": phrase, "pred": prediction, "proba": best_proba, "feedback": correct, "timestamp":now}
    insertion = predictions.insert_one(feedback_data)

    if insertion.acknowledged:
        return render_template("submission.html", message="Données enregistrées avec succès !")
    else:
        return render_template("submission.html", message="Erreur lors de l'enregistrement des données.")

if __name__ == '__main__':
    app.run(debug=True)
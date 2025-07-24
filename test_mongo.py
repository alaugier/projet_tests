import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables d'environnement
HOST_MONGODB = os.getenv("HOST_MONGODB")
MONGO_DB_APPNAME = os.getenv("CLUSTER_NAME_MONGODB")
PASSWORD_MONGODB = os.getenv("PASSWORD_MONGODB")
USER_MONGODB = os.getenv("USER_MONGODB")

print("=== Test de connexion MongoDB Atlas ===\n")

# Vérifier que toutes les variables sont présentes
print("1. Vérification des variables d'environnement:")
variables = {
    "HOST_MONGODB": HOST_MONGODB,
    "CLUSTER_NAME_MONGODB": MONGO_DB_APPNAME,
    "USER_MONGODB": USER_MONGODB,
    "PASSWORD_MONGODB": "***" if PASSWORD_MONGODB else None
}

for var_name, var_value in variables.items():
    if var_value:
        print(f"   ✅ {var_name}: {var_value}")
    else:
        print(f"   ❌ {var_name}: MANQUANT")

print()

# Test de connexion
print("2. Test de connexion:")
uri = f"mongodb+srv://{USER_MONGODB}:{PASSWORD_MONGODB}@{HOST_MONGODB}/?retryWrites=true&w=majority&appName={MONGO_DB_APPNAME}"

try:
    # Créer le client MongoDB
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Tester la connexion
    client.admin.command('ping')
    print("   ✅ Connexion MongoDB réussie !")
    
    # Tester l'accès à la base de données
    print("\n3. Test d'accès à la base de données:")
    db = client.nlp_classification
    predictions = db.predictions
    print("   ✅ Accès à la base 'nlp_classification' et collection 'predictions'")
    
    # Test d'insertion (optionnel)
    print("\n4. Test d'insertion d'un document de test:")
    test_doc = {
        "phrase": "Test de connexion",
        "pred": 1,
        "proba": 0.95,
        "feedback": True,
        "timestamp": datetime.now().strftime("%Y_%m_%d__%H_%M_%S"),
        "test": True  # Pour identifier les documents de test
    }
    
    result = predictions.insert_one(test_doc)
    if result.acknowledged:
        print(f"   ✅ Document de test inséré avec ID: {result.inserted_id}")
        
        # Supprimer le document de test
        predictions.delete_one({"_id": result.inserted_id})
        print("   ✅ Document de test supprimé")
    else:
        print("   ❌ Échec de l'insertion du document de test")
    
    print("\n🎉 Tous les tests sont passés ! MongoDB Atlas est prêt.")
    
except Exception as e:
    print(f"   ❌ Erreur de connexion MongoDB : {e}")
    print("\n💡 Vérifiez :")
    print("   - Vos identifiants dans le fichier .env")
    print("   - Que votre IP est autorisée dans MongoDB Atlas")
    print("   - Que votre cluster est actif")

finally:
    try:
        client.close()
    except:
        pass
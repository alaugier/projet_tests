# 🧠 NLP Classification App
Application Flask permettant la classification de phrases en utilisant un modèle de régression logistique pré-entraîné, avec enregistrement des feedbacks utilisateurs dans MongoDB Atlas.

---
[![Tests CI](https://github.com/alaugier/projet_tests/actions/workflows/main.yml/badge.svg)](https://github.com/alaugier/projet_tests/actions/workflows/main.yml)
[![Deploy to Render](https://img.shields.io/badge/render-deployed-brightgreen?logo=render)](https://dashboard.render.com/web/services)

---
## 🚀 Démo en ligne
🔗 [Lien vers l'application sur Render](https://ton-app.render.com) ← *(remplacer dès que le déploiement est actif)*

---
## 📦 Fonctionnalités
- Interface simple avec Flask pour soumettre des phrases
- Prédiction du modèle (régression logistique entraîné avec TF-IDF)
- Enregistrement des retours utilisateurs dans MongoDB Atlas (`predictions`)
- Tests unitaires avec `pytest` pour garantir la fiabilité
- Déploiement automatique via GitHub Actions + Render

---
## 🛠️ Installation locale
```bash
# 1. Cloner le dépôt
git clone https://github.com/alaugier/projet_tests.git
cd projet_tests

# 2. Créer et activer un environnement virtuel
python -m venv env
source env/bin/activate  # sous Windows : env\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer un fichier .env à la racine avec les informations MongoDB
cp .env.example .env
# ...puis modifier le contenu avec les vraies informations

# 5. Lancer l'application
python app/app.py
```

## 🧪 Lancer les tests
```bash
pytest app/tests
```

## ⚙️ Structure du projet
```bash
projet_tests/
├── app/
│   ├── app.py
│   ├── models/
│   ├── templates/
│   └── tests/
├── .github/workflows/main.yml
├── .env.example
├── requirements.txt
└── README.md
```

## 📤 Déploiement continu
- CI avec GitHub Actions
- Déploiement automatique via Render sur chaque push sur la branche main

## 🙌 Remerciements
Projet personnel réalisé dans le cadre d'une mise en œuvre de tests automatisés et déploiement CI/CD.
Modèle entraîné localement puis utilisé pour classification.
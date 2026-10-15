Restaurant Suggester AI

Chatbot qui recommande le meilleur restaurant selon le plat, le budget, l'ambiance et la ville, à partir d'une base de données locale (100 restaurants à Alger et Blida). La réponse est générée en Darija (lettres latines) par un modèle local via Ollama, et un bouton ouvre directement le restaurant dans Google Maps.

Fonctionnalités
Questionnaire en 4 étapes : cuisine, budget, ambiance, localisation (avec option « Autre (préciser)… »)
Filtrage par ville en Python avant l'appel au modèle
Recommandation par un LLM local (qwen2.5:7b), limitée aux restaurants du JSON
Bouton 📍 Ouvrir dans Google Maps après chaque recherche
Historique des recherches dans la sidebar (avec lien Maps)
Bouton New Chat pour recommencer
Interface personnalisée (image de fond, cartes translucides) via style.css
Structure du projet
.
├── app.py             # Interface Streamlit + logique des étapes
├── prompts.py         # Prompt système envoyé au modèle
├── restaurants.json   # Base de données des restaurants
├── style.css          # Thème de l'interface
└── README.md
Prérequis
Python 3.9+
Ollama installé et lancé
Le modèle qwen2.5:7b
Installation
bash
# 1. Installer les dépendances Python
pip install streamlit ollama

# 2. Télécharger le modèle
ollama pull qwen2.5:7b
Lancement
bash
# Ollama doit tourner en arrière-plan (ollama serve)
streamlit run app.py

L'application s'ouvre sur http://localhost:8501.

À propos de maps_link

Les liens actuels sont des recherches Google Maps (nom + ville). Pour un lien exact, remplace la valeur par le lien de partage du lieu (https://maps.app.goo.gl/...).

Comment ça marche
L'utilisateur répond aux 4 questions (st.session_state garde les choix).
app.py filtre restaurants.json par ville.
prompts.py construit le prompt système avec la liste filtrée (sans maps_link).
Ollama choisit le meilleur restaurant et répond en Darija.
app.py retrouve le restaurant cité dans la réponse et affiche le bouton Google Maps.
Personnalisation
Changer de modèle : modifier model="qwen2.5:7b" dans app.py.
Ajouter une ville : ajouter les restaurants dans le JSON, puis une option dans l'étape 4 et une condition dans le filtrage de l'étape 5.
Changer le style : modifier style.css (couleurs, image de fond, boutons).

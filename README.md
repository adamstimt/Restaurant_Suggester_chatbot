
#  Restaurant Suggester AI

> Chatbot intelligent qui recommande le meilleur restaurant selon le plat, le budget, l'ambiance et la ville, à partir d'une base de données locale (**100 restaurants à Alger et Blida**). 

La réponse est générée en **Darija (lettres latines)** par un modèle local via **Ollama**, et un bouton interactif permet d'ouvrir directement le restaurant sur **Google Maps**.

---

##  Fonctionnalités

* **Questionnaire en 4 étapes** : Cuisine, budget, ambiance et localisation (avec option personnalisée « *Autre (préciser)…* »).
* **Filtrage hybride intelligent** : Filtrage préalable par ville en Python avant l'appel au modèle pour éliminer les hallucinations géographiques.
* **Inférence locale (LLM)** : Propulsé par `qwen2.5:7b` via Ollama (respect total de la vie privée, zéro dépendance cloud).
* **Intégration Google Maps** : Bouton dynamique 📍 *Ouvrir dans Google Maps* généré automatiquement après chaque recherche.
* **Historique & Navigation** : Suivi des recherches précédentes dans la barre latérale avec persistance des liens Maps, et bouton *New Chat* pour recommencer.
* **UI Ultra-Moderne** : Design Glassmorphism sombre personnalisé via un fichier `style.css` externe (image de fond, cartes translucides, effets de survol).

---

## 📂 Structure du Projet

```text
res-bot/
│
├── app.py              # Interface Streamlit + logique des étapes et gestion de session
├── prompts.py          # Prompt système envoyé au modèle
├── restaurants.json    # Base de données locale de 100+ restaurants avec liens Maps
├── style.css           # Thème de l'interface (Glassmorphism dark mode)
└── README.md           # Documentation du projet
```

---

##  Prérequis

* **Python 3.9+**
* **Ollama** installé et configuré localement.
* Le modèle **Qwen 2.5 (7B)** téléchargé.

---

##  Installation & Lancement

### 1. Installer les dépendances Python
Ouvre ton terminal dans le dossier du projet et exécute :
```bash
pip install streamlit ollama
```

### 2. Télécharger le modèle LLM
Assure-toi de télécharger le modèle Qwen 2.5 via Ollama :
```bash
ollama pull qwen2.5:7b
```

### 3. Lancer l'application
Démarre le service Ollama en arrière-plan (si ce n'est pas déjà fait) :
```bash
ollama serve
```
Puis, lance l'application Streamlit :
```bash
streamlit run app.py
```
L'application s'ouvrira automatiquement dans ton navigateur sur **`http://localhost:8501`**.

---

##  Comment ça marche ?

1. L'utilisateur répond aux 4 questions du questionnaire interactif (les choix sont sauvegardés via `st.session_state`).
2. `app.py` filtre dynamiquement le fichier `restaurants.json` en fonction de la ville choisie.
3. `prompts.py` construit le prompt système en intégrant uniquement la liste filtrée.
4. Ollama analyse les critères, sélectionne le meilleur restaurant et répond en **Darija**.
5. L'application récupère le restaurant cité dans la réponse et affiche le bouton d'accès direct à Google Maps.

> **Note sur `maps_link`** : Les liens actuels sont des recherches Google Maps automatisées (`nom + ville`). Pour un emplacement exact, remplace la valeur dans le JSON par le lien de partage officiel du lieu (`https://maps.app.goo.gl/...`).

---

##  Personnalisation

* **Changer de modèle** : Modifie `model="qwen2.5:7b"` dans le fichier `app.py`.
* **Ajouter une ville** : Ajoute de nouveaux restaurants dans `restaurants.json`, puis intègre l'option correspondante à l'étape 4 et ajuste la condition de filtrage à l'étape 5 dans `app.py`.
* **Modifier le design** : Édite le fichier `style.css` (couleurs, arrière-plan, typographie, ombres).

---


import streamlit as st
import json
import ollama
from prompts import get_simple_prompt

# 1. Configuration de la page
st.set_page_config(
    page_title="Restaurant Suggester AI",
    page_icon="🍔",
    layout="centered"
)

# 2. Chargement du fichier CSS externe
def load_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Fichier style.css introuvable.")

load_css("style.css")

# 3. Chargement de la BDD JSON
@st.cache_data
def load_restaurants():
    try:
        with open("restaurants.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Fichier 'restaurants.json' introuvable !")
        return []

restaurants_db = load_restaurants()

# 4. Initialisation des variables de Session State
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_choices" not in st.session_state:
    st.session_state.user_choices = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------------
# SIDEBAR : New Chat & Historique
# ---------------------------------------------------------
with st.sidebar:
   
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.step = 1
        st.session_state.user_choices = {}
        st.rerun()

    if not st.session_state.chat_history:
        st.caption("Aucune recherche enregistrée.")
    else:
        for idx, item in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"🔍 {item['choices']['plat']} ({item['choices']['ville']})"):
                st.write(f"**Budget:** {item['choices']['budget']}")
                st.write(f"**Ambiance:** {item['choices']['moral']}")
                st.markdown("---")
                st.markdown(item["response"])
                if item.get("maps_link"):
                    st.link_button("📍 Google Maps", item["maps_link"], key=f"map_{idx}")

# ---------------------------------------------------------
# PAGE PRINCIPALE
# ---------------------------------------------------------
st.title("🍔 Restaurant Suggester AI")

# --- ÉTAPE 1: Choix du Plat ---
if st.session_state.step == 1:
    st.subheader("1️⃣ Que souhaites-tu manger aujourd'hui ?")
    plat_option = st.radio(
        "Choisis un type de cuisine :",
        [
            "Fast Food / Tacos / Burgers",
            "Pizza / Cuisine Italienne",
            "Cuisine Traditionnelle Algérienne",
            "Grillades / Barbecue",
            "Poisson / Fruits de mer",
            "Café / Desserts / Crêpes",
            "Autre (préciser)..."
        ],
        index=0
    )
    
    custom_plat = ""
    if plat_option == "Autre (préciser)...":
        custom_plat = st.text_input("Précise ton envie (ex: Sushi, Sandwich kefta, Karantika...) :")

    if st.button("Suivant ➡️", key="step1"):
        final_plat = custom_plat if plat_option == "Autre (préciser)..." and custom_plat else plat_option
        st.session_state.user_choices["plat"] = final_plat
        st.session_state.step = 2
        st.rerun()

# --- ÉTAPE 2: Choix du Budget ---
elif st.session_state.step == 2:
    st.subheader("2️⃣ Quel est ton budget ?")
    budget_option = st.radio(
        "Sélectionne ta tranche de prix :",
        [
            "📉 Économique (Moins de 1000 DA)",
            "⚖️ Moyen (Entre 1000 DA et 3000 DA)",
            "💎 Haut de gamme (Plus de 3000 DA)",
            "Autre (préciser)..."
        ],
        index=0
    )

    custom_budget = ""
    if budget_option == "Autre (préciser)...":
        custom_budget = st.text_input("Précise ton budget (ex: Max 1500 DA...) :")

    if st.button("Suivant ➡️", key="step2"):
        if budget_option == "Autre (préciser)..." and custom_budget:
            final_budget = custom_budget
        elif "Économique" in budget_option:
            final_budget = "Cheap"
        elif "Moyen" in budget_option:
            final_budget = "Medium"
        else:
            final_budget = "High"

        st.session_state.user_choices["budget"] = final_budget
        st.session_state.step = 3
        st.rerun()

# --- ÉTAPE 3: Choix de l'Humeur / Ambiance ---
elif st.session_state.step == 3:
    st.subheader("3️⃣ Quelle est ton humeur / ambiance recherchée ?")
    moral_option = st.radio(
        "Choisis l'ambiance idéale :",
        [
            "⚡ Rapide et gourmand (Pressé / Envie de manger vite)",
            "👨‍👩‍👧‍👦 Familial et calme (Pour sortir en famille ou entre amis)",
            "✨ Chic et élégant (Pour une occasion spéciale)",
            "🌲 En plein air / Nature (Vue panoramique / Terrasse)",
            "Autre (préciser)..."
        ],
        index=0
    )

    custom_moral = ""
    if moral_option == "Autre (préciser)...":
        custom_moral = st.text_input("Précise ton humeur (ex: Endroit pour étudier...) :")

    if st.button("Suivant ➡️", key="step3"):
        final_moral = custom_moral if moral_option == "Autre (préciser)..." and custom_moral else moral_option
        st.session_state.user_choices["moral"] = final_moral
        st.session_state.step = 4
        st.rerun()

# --- ÉTAPE 4: Choix de la Localisation ---
elif st.session_state.step == 4:
    st.subheader("4️⃣ Dans quelle ville ou zone cherches-tu ?")
    ville_option = st.radio(
        "Sélectionne la localisation :",
        [
            "Alger (Algiers)",
            "Blida",
            "Peu importe (N'importe quelle ville)",
            "Autre (préciser)..."
        ],
        index=0
    )

    custom_ville = ""
    if ville_option == "Autre (préciser)...":
        custom_ville = st.text_input("Précise la commune (ex: Hydra, Boufarik, Kouba...) :")

    if st.button("Lancer la recherche 🎯", key="step4"):
        final_ville = custom_ville if ville_option == "Autre (préciser)..." and custom_ville else ville_option
        st.session_state.user_choices["ville"] = final_ville
        st.session_state.step = 5
        st.rerun()

# --- ÉTAPE 5: Génération du Résultat & Historique ---
elif st.session_state.step == 5:
    st.subheader("🎯 Le meilleur restaurant selon tes critères :")
    
    choices = st.session_state.user_choices
    
    st.info(
        f"📌 **Tes critères :**  \n"
        f"- **Plat / Cuisine :** `{choices['plat']}`  \n"
        f"- **Budget :** `{choices['budget']}`  \n"
        f"- **Ambiance :** `{choices['moral']}`  \n"
        f"- **Localisation :** `{choices['ville']}`"
    )

    # Filtrage préalable par ville avec Python
    filtered_db = []
    target_ville = choices['ville'].lower()
    
    for r in restaurants_db:
        r_city = r.get("city", "").lower()
        if "alger" in target_ville and r_city != "algiers":
            continue
        elif "blida" in target_ville and r_city != "blida":
            continue
        filtered_db.append(r)

    if not filtered_db:
        filtered_db = restaurants_db

    user_summary_prompt = f"""
    Voici les critères souhaités :
    - Cuisine/Plat recherché : {choices['plat']}
    - Budget : {choices['budget']}
    - Ambiance / Vibe : {choices['moral']}
    - Ville : {choices['ville']}

    Choisis le MEILLEUR restaurant de la liste fournie dans le system prompt.
    """

    system_prompt = get_simple_prompt(filtered_db)

    with st.spinner("Recherche du restaurant idéal dans la base de données..."):
        try:
            response = ollama.chat(
                model="qwen2.5:7b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_summary_prompt}
                ]
            )
            bot_reply = response["message"]["content"]
            st.markdown(bot_reply)

            # Retrouver le restaurant recommandé (nom le plus long trouvé dans la réponse)
            matches = [r for r in filtered_db if r["name"].lower() in bot_reply.lower()]
            if matches:
                chosen = max(matches, key=lambda r: len(r["name"]))
                st.link_button("📍 Ouvrir dans Google Maps", chosen["maps_link"], use_container_width=True)

            # Sauvegarde dans l'historique
            if "last_saved" not in st.session_state or st.session_state.last_saved != choices:
                st.session_state.chat_history.append({
                    "choices": choices,
                    "response": bot_reply,
                    "maps_link": chosen["maps_link"] if matches else None
                })
                st.session_state.last_saved = choices

        except Exception as e:
            st.error(f"Erreur de connexion avec Ollama : {e}")

    if st.button("🔄 Refaire une recherche"):
        st.session_state.step = 1
        st.session_state.user_choices = {}
        st.rerun()
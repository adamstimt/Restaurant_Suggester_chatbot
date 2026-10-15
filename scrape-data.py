import time
import json
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def defiler_flux(driver, element_flux, nombre_cible=50):
    """Fait défiler la liste dans Google Maps pour charger suffisamment de restaurants."""
    derniere_hauteur = 0
    tentatives = 0
    while tentatives < 15:
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", element_flux
        )
        time.sleep(2.5)
        
        elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        if len(elements) >= nombre_cible:
            break
            
        nouvelle_hauteur = driver.execute_script("return arguments[0].scrollHeight", element_flux)
        if nouvelle_hauteur == derniere_hauteur:
            tentatives += 1
        else:
            tentatives = 0
        derniere_hauteur = nouvelle_hauteur

def scraper_google_maps():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    tous_les_restaurants = []
    id_actuel = 1

    # Pools de données pour diversifier aléatoirement chaque restaurant
    pool_cuisines = [
        "Fast Food / Tacos / Burgers",
        "Pizza / Cuisine Italienne",
        "Cuisine Traditionnelle Algérienne",
        "Grillades / Barbecue",
        "Poisson / Fruits de mer",
        "Café / Desserts / Crêpes"
    ]
    
    pool_budgets = ["Cheap", "Medium", "High"]
    
    pool_ambiances = [
        "⚡ Rapide et gourmand (Pressé / Envie de manger vite)",
        "👨‍👩‍👧‍👦 Familial et calme (Pour sortir en famille ou entre amis)",
        "✨ Chic et élégant (Pour une occasion spéciale)",
        "🌲 En plein air / Nature (Vue panoramique / Terrasse)"
    ]

    recherches = [
        {"requete": "restaurants in Algiers", "ville": "Algiers"},
        {"requete": "restaurants in Blida", "ville": "Blida"}
    ]

    for info in recherches:
        requete = info["requete"]
        ville = info["ville"]
        print(f"\n🔍 Recherche et extraction des données pour : {ville}...")
        
        driver.get(f"https://www.google.com/maps/search/{requete}")
        time.sleep(5)

        try:
            flux = driver.find_element(By.XPATH, '//div[@role="feed"]')
            print("⏳ Défilement en cours pour charger au moins 50 restaurants...")
            defiler_flux(driver, flux, nombre_cible=50)
        except Exception as e:
            print(f"⚠️ Avertissement lors du défilement automatique : {e}")

        resultats = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        print(f"📍 {len(resultats)} éléments trouvés. Extraction et diversification en cours...")

        compteur = 0
        for r in resultats:
            if compteur >= 50:
                break
                
            try:
                aria_label = r.get_attribute("aria-label")
                maps_link = r.get_attribute("href")
                
                if aria_label and maps_link:
                    nom_nettoye = aria_label.split(',')[0].strip()
                    
                    # Extraction de la note si elle existe
                    note = "4.2"
                    match = re.search(r'\b([0-9][,\.][0-9])\b', aria_label)
                    if match:
                        note = match.group(1).replace(',', '.')

                    # Sélection aléatoire des caractéristiques pour un bon équilibre
                    cuisine_selectionnee = random.choice(pool_cuisines)
                    budget_selectionne = random.choice(pool_budgets)
                    ambiance_selectionnee = random.choice(pool_ambiances)

                    entree_restaurant = {
                        "id": id_actuel,
                        "name": nom_nettoye,
                        "cuisine": cuisine_selectionnee,
                        "budget": budget_selectionne,
                        "vibe": ambiance_selectionnee,
                        "city": ville,
                        "rating": note,
                        "description": f"Découvrez {nom_nettoye} à {ville}, un endroit idéal spécialisé en {cuisine_selectionnee.lower()}.",
                        "maps_link": maps_link
                    }
                    
                    tous_les_restaurants.append(entree_restaurant)
                    id_actuel += 1
                    compteur += 1
            except Exception as ex:
                continue

    driver.quit()

    nom_fichier_sortie = "restaurants.json"
    with open(nom_fichier_sortie, "w", encoding="utf-8") as f:
        json.dump(tous_les_restaurants, f, ensure_ascii=False, indent=4)

    print(f"\n Opération réussie ! {len(tous_les_restaurants)} restaurants enregistrés dans '{nom_fichier_sortie}' avec un contenu entièrement en français.")

if __name__ == "__main__":
    scraper_google_maps()
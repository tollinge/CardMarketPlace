from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tabulate import tabulate
import time
import json


options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

base_url = "https://tradingcardmarket.com/collections/trading-card-games?page="
page = 1
all_products = []

try:
    while True:
        url = base_url + str(page)
        print(f"[+] Chargement de la page {page}...")

        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(1.5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        products = soup.select("li.ss__result")

        if not products:
            print(f"[!] Aucune donnée sur la page {page}. Fin du scraping.")
            break

        for p in products:
            a_tag = p.select_one("h3.card__heading a")
            name = a_tag.text.strip() if a_tag else "N/A"

            price_tag = p.select_one("span.price-item--regular")
            if not price_tag:
                continue  # produit sans prix = on skippe

            price_str = price_tag.text.strip().replace("$", "").replace(",", "")
            try:
                price = float(price_str)
            except ValueError:
                continue  # prix invalide = on skippe

            all_products.append((name, price))

        page += 1

    # ✅ Trier par prix décroissant
    all_products.sort(key=lambda x: x[1], reverse=True)

    # ✅ Ajouter numéro de rang
    rows = [[i+1, name, f"${price:.2f}"] for i, (name, price) in enumerate(all_products)]

    # ✅ Afficher tableau
    headers = ["#", "Name", "Price"]
    print(f"\n✅ {len(all_products)} produits récupérés sur {page - 1} pages (triés par prix décroissant).\n")
    print(tabulate(rows, headers=headers, tablefmt="pretty"))

finally:
    # ✅ Sauvegarder les produits dans un fichier JSON
    json_data = [
        {"rank": i + 1, "name": name, "price": price}
        for i, (name, price) in enumerate(all_products)
    ]

    with open(".venv/products.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("\n✅ Données sauvegardées dans 'products.json'")

    driver.quit()

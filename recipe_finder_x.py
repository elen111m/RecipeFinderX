import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("EDAMAM_APP_ID")
APP_KEY = os.getenv("EDAMAM_APP_KEY")
BASE_URL = "https://api.edamam.com/search"

def require_creds():
    if not APP_ID or not APP_KEY:
        print("Missing credentials. Please set EDAMAM_APP_ID and EDAMAM_APP_KEY in a .env file.")
        sys.exit(1)

def search_recipes(query: str, start: int = 0, end: int = 20):
    params = {"q": query, "app_id": APP_ID, "app_key": APP_KEY, "from": start, "to": end}
    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"Error: {e}")
        return []

    hits = data.get("hits", [])
    results = []
    for hit in hits:
        rec = hit.get("recipe", {})
        label = rec.get("label", "Unknown")
        url = rec.get("url", "")
        calories_total = float(rec.get("calories", 0.0))
        servings = rec.get("yield")
        health = rec.get("healthLabels", [])
        results.append(
            {
                "label": label,
                "url": url,
                "calories_total": calories_total,
                "servings": servings,
                "calories_per_serving": (calories_total / float(servings)) if servings else None,
                "health": health[:5],
            }
        )
    return results

def pretty_print(recipes):
    if not recipes:
        print("No recipes found.")
        return
    for i, r in enumerate(recipes, 1):
        if r["calories_per_serving"]:
            calories = f"{r['calories_per_serving']:.0f} kcal/serving"
        else:
            calories = f"{r['calories_total']:.0f} kcal total"
        health = ", ".join(r["health"]) if r["health"] else "—"
        print(f"{i}. {r['label']}\n   {calories}\n   Health: {health}\n   {r['url']}\n")

def main():
    require_creds()
    query = " ".join(sys.argv[1:]).strip() or input("Enter an ingredient: ").strip()
    if not query:
        print("Please provide a search term.")
        sys.exit(1)

    recipes = search_recipes(query)
    if not recipes:
        retry = input("Nothing found. Try again? (y/N): ").strip().lower()
        if retry == "y":
            query = input("Enter an ingredient: ").strip()
            recipes = search_recipes(query)

    pretty_print(recipes)

if __name__ == "__main__":
    main()


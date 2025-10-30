import fastapi
import requests
from fastapi.middleware.cors import CORSMiddleware

url = "https://pokeapi.co/api/v2/"
app = fastapi.FastAPI()

# Modifico il middleware CORS per consentire tutte le origini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consenti tutte le origini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pokemon/{identifier}")
def get_pokemon(identifier: str):
    response = requests.get(f"{url}pokemon/{identifier.lower()}")
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "base_experience": data["base_experience"],
            "height": data["height"],
            "is_default": data["is_default"],
            "order": data["order"],
            "weight": data["weight"],
            "abilities": [
                {
                    "is_hidden": ability["is_hidden"],
                    "slot": ability["slot"],
                    "ability": ability["ability"]
                }
                for ability in data["abilities"]
            ],
            "forms": data["forms"],
            "game_indices": data["game_indices"],
            "stats": [
                {
                    "base_stat": stat["base_stat"],
                    "effort": stat["effort"],
                    "stat": stat["stat"]
                }
                for stat in data["stats"]
            ],
            "types": [
                {
                    "slot": type_["slot"],
                    "type": type_["type"]
                }
                for type_ in data["types"]
            ],
            "sprites": data["sprites"]
        }
    else:
        return {"error": "Pokémon not found"}

@app.get("/ability/{identifier}")
def get_ability(identifier: str):
    response = requests.get(f"{url}ability/{identifier.lower()}")
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "is_main_series": data["is_main_series"],
            "generation": data["generation"],
            "names": data["names"],
            "effect_entries": data["effect_entries"],
            "pokemon": [
                {
                    "is_hidden": pokemon["is_hidden"],
                    "slot": pokemon["slot"],
                    "pokemon": pokemon["pokemon"]
                }
                for pokemon in data["pokemon"]
            ]
        }
    else:
        return {"error": "Ability not found"}

@app.get("/type/{identifier}")
def get_type(identifier: str):
    response = requests.get(f"{url}type/{identifier.lower()}")
    if response.status_code == 200:
        data = response.json()
        return {
            "id": data["id"],
            "name": data["name"],
            "damage_relations": data["damage_relations"],
            "pokemon": data["pokemon"],
            "moves": data["moves"]
        }
    else:
        return {"error": "Type not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


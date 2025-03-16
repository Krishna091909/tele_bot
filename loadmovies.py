import json

def load_movies():
    try:
        with open("movies.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_movies(movies):
    print("DEBUG: Saving movies.json...")  # Debugging line
    with open("movies.json", "w") as file:
        json.dump(movies, file, indent=4)
    print("DEBUG: Saved successfully!")  # Confirm it is saving

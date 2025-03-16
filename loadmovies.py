import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Load credentials from Render environment variable
CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not CREDENTIALS_JSON:
    raise ValueError("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable is missing!")

# Convert JSON string to dictionary
creds_dict = json.loads(CREDENTIALS_JSON)

# Authenticate with Google Sheets
creds = Credentials.from_service_account_info(creds_dict, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])
client = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = "1ZBNk7zJ5bPHhfb2UgLPC27A-phWkhlvtBHiHH_JjsyU"  # Replace with your actual Sheet ID
sheet = client.open_by_key(SHEET_ID).sheet1

# Load movies from Google Sheets
def load_movies():
    movies = {}
    data = sheet.get_all_records()
    for row in data:
        if "Movie Name" in row and "File ID" in row and "File Size" in row and "File Name" in row:
            movies[row["Movie Name"]] = {
                "file_id": row["File ID"],
                "file_size": row["File Size"],
                "file_name": row["File Name"]
            }
        else:
            print(f"⚠️ Skipping invalid row: {row}")  # Debugging message
    return movies

# Save movie to Google Sheets
def save_movie(movie_name, file_id, file_size, file_name):
    sheet.append_row([movie_name, file_id, file_size, file_name])

# Remove movie from Google Sheets
def remove_movie(movie_name):
    records = sheet.get_all_values()
    for i, row in enumerate(records):
        if row and row[0] == movie_name:
            sheet.delete_rows(i + 1)
            return True
    return False

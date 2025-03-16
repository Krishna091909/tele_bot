import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API Authentication
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"  # Your credentials file

# Connect to Google Sheets
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open your sheet (Replace with your sheet name)
SHEET_NAME = "MoviesDatabase"
sheet = client.open(SHEET_NAME).sheet1  

def load_movies():
    """Load movies from Google Sheet."""
    movies = {}
    data = sheet.get_all_values()  # Get all rows
    for row in data[1:]:  # Skip header
        movie_name, file_id, file_size, file_name = row
        movies[movie_name] = {
            "file_id": file_id,
            "file_size": file_size,
            "file_name": file_name
        }
    return movies

def save_movies(movies):
    """Save movies to Google Sheet (Rewrites the entire sheet)."""
    sheet.clear()  # Clear the existing data
    sheet.append_row(["Movie Name", "File ID", "File Size", "File Name"])  # Header
    for movie, details in movies.items():
        sheet.append_row([movie, details["file_id"], details["file_size"], details["file_name"]])

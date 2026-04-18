import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

def get_gspread_client():

    try:
        credentials = Credentials.from_service_account_file(
            filename=CREDENTIALS_PATH,
            scopes=SCOPES
        )
        print("Authorizing gspread for data export service...")
        return gspread.authorize(credentials)

    except Exception as e:
        raise Exception(f"Failed authenticating gspread: {e}")
import os
import gspread
from google.oauth2.service_account import Credentials

# === CONFIGURATION ===
SHEET_NAME = "Prasad Auto Parts"  # Name of your Google Sheet
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def test_connection():
    """Test connection and write a sample row to verify Google Sheets access."""
    print("🔍 Checking Google Sheets connection...")
    print(f"📄 Credentials file: {CREDENTIALS_FILE}")

    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ ERROR: credentials.json not found.")
        return

    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1
        print(f"✅ Connected to Google Sheet: '{SHEET_NAME}'")

        # Ensure header row exists
        headers = sheet.row_values(1)
        if not headers:
            headers = [
                "Customer Name", "Phone", "Email", "Vehicle Model",
                "Registration No", "Services", "Date", "Time Slot", "Notes"
            ]
            sheet.append_row(headers)
            print("🧾 Header row created:", headers)

        # Add a test row
        test_row = [
            "Test User", "9999999999", "test@example.com",
            "Honda Activa", "MH12AB1234", "Oil Change",
            "2025-11-01", "10:30 AM", "Test entry from script"
        ]
        sheet.append_row(test_row)
        print("✅ Test row successfully appended!")
        print(test_row)

        print("\n🚀 Google Sheets integration is working perfectly!")

    except Exception as e:
        print("❌ ERROR connecting to Google Sheets:")
        print(e)


if __name__ == "__main__":
    test_connection()

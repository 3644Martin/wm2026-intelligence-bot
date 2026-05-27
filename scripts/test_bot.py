import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = "8954365774:AAHEUSzyaZtHDpurIEdGZ3-1XPhLxu-ihvk"
CHAT_ID = "6624173034"

message = "⚽ WM 2026 Intelligence Bot erfolgreich verbunden!"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(telegram_url, data={
    "chat_id": CHAT_ID,
    "text": message
})

print("Telegram Nachricht gesendet")

# =========================
# GOOGLE SHEETS
# =========================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("WM2026_Tippspiel_Intelligence")

worksheet = sheet.worksheet("News")

worksheet.append_row([
    "2026-05-27",
    "Germany",
    "Test",
    "Bot successfully connected",
    "Low",
    "System",
    "-"
])

print("Google Sheet erfolgreich aktualisiert")

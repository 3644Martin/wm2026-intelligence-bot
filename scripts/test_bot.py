# ==========================================
# WM 2026 Intelligence Bot - Test Script
#
# Purpose:
# Verify that all core integrations work correctly.
#
# This script tests:
#
# 1. Loading environment variables (.env)
# 2. Telegram Bot connectivity
# 3. Google Sheets authentication
# 4. Writing data into Google Sheets
#
# Expected result:
# - Telegram test message received
# - New row added to News worksheet
#
# This script is used for:
# - initial setup validation
# - debugging
# - connectivity testing
#
# ==========================================
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

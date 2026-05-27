import os
from datetime import datetime, timezone

import feedparser
import gspread
import requests
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_NAME = "WM2026_Tippspiel_Intelligence"

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "https://www.espn.com/espn/rss/soccer/news",
    "https://www.kicker.de/news/fussball/rss",
]

IMPORTANT_KEYWORDS = [
    "injury", "injured", "doubt", "out", "suspended", "squad", "lineup",
    "verletzung", "verletzt", "fraglich", "gesperrt", "kader", "aufstellung",
    "world cup", "wm 2026", "fifa world cup", "weltmeisterschaft",
]


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram skipped: BOT_TOKEN or CHAT_ID missing")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope,
    )

    client = gspread.authorize(creds)
    return client.open(SHEET_NAME)


def is_important(text):
    text = text.lower()
    return any(keyword in text for keyword in IMPORTANT_KEYWORDS)


def main():
    sheet = connect_sheet()
    news_ws = sheet.worksheet("News")
    alerts_ws = sheet.worksheet("Alerts")

    existing_urls = set()
    existing_rows = news_ws.get_all_records()

    for row in existing_rows:
        url = row.get("URL")
        if url:
            existing_urls.add(url)

    added_count = 0
    alert_count = 0

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        source_name = feed.feed.get("title", feed_url)

        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            if not title or not link:
                continue

            if link in existing_urls:
                continue

            combined_text = f"{title} {summary}"
            important = is_important(combined_text)
            impact = "High" if important else "Low"

            now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

            news_ws.append_row([
                now,
                "",
                "News",
                title,
                impact,
                source_name,
                link,
            ])

            added_count += 1

            if important:
                alerts_ws.append_row([
                    now,
                    "IMPORTANT",
                    "",
                    title,
                    "Yes",
                    source_name,
                ])

                send_telegram(
                    f"🚨 WM 2026 Alert\n\n{title}\n\nSource: {source_name}\n{link}"
                )

                alert_count += 1

    send_telegram(
        f"✅ WM News Update completed\n\nNews added: {added_count}\nAlerts sent: {alert_count}"
    )

    print(f"News added: {added_count}")
    print(f"Alerts sent: {alert_count}")


if __name__ == "__main__":
    main()
import os
import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

URL = "https://wtblizzcon.com/available-tickets/"

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

STATE_FILE = "last_hash.txt"


def send_email(body):
    msg = MIMEText(body)

    msg["Subject"] = "🎟️ BlizzCon Tickets Available!"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)


response = requests.get(URL, headers=HEADERS, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text(" ", strip=True)

tickets_available = (
    "There are currently no tickets available"
    not in text
)

page_hash = hashlib.sha256(text.encode()).hexdigest()

previous_hash = ""

if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        previous_hash = f.read().strip()

if tickets_available and page_hash != previous_hash:

    send_email(
f"""
BlizzCon tickets may be available!

Visit:

{URL}
"""
    )

with open(STATE_FILE, "w") as f:
    f.write(page_hash)

print("Finished.")

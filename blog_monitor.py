"""
Blog Monitor for amdrodd.com/blog
Reads credentials from environment variables (GitHub Secrets).
Emails you the latest blog post.
"""

import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

BLOG_URL        = "https://amdrodd.com/blog"
YOUR_EMAIL      = os.environ["YOUR_EMAIL"]
SENDER_EMAIL    = os.environ["SENDER_EMAIL"]
SENDER_APP_PASS = os.environ["SENDER_APP_PASS"]

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def fetch_latest_post():
    headers = {"User-Agent": "Mozilla/5.0 (blog-monitor-bot)"}
    resp = requests.get(BLOG_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for heading in soup.find_all(["h2", "h3"]):
        link = heading.find("a", href=True)
        if link and "amdrodd.com" in link["href"]:
            title = link.get_text(strip=True)
            url   = link["href"]
            if title:
                return title, url
    return None, None

def send_email(title, url):
    subject = f"Latest Blog Post: {title}"

    body_text = f"Latest blog post on amdrodd.com:\n\n{title}\n{url}"
    body_html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:20px">
      <h2>Latest post on <a href="{BLOG_URL}">amdrodd.com/blog</a></h2>
      <p><a href="{url}" style="font-size:18px">{title}</a></p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = YOUR_EMAIL
    msg.attach(MIMEText(body_text, "plain"))
    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_APP_PASS)
        server.sendmail(SENDER_EMAIL, YOUR_EMAIL, msg.as_string())

    print(f"Email sent to {YOUR_EMAIL}!")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Checking {BLOG_URL} ...")
    title, url = fetch_latest_post()
    if title:
        print(f"Latest post: {title}")
        print(f"URL: {url}")
        send_email(title, url)
    else:
        print("No posts found.")

if __name__ == "__main__":
    main()

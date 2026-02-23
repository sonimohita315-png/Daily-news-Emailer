import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from google import genai

# ── CONFIG (loaded from GitHub Secrets — don't put real values here) ──
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
YOUR_EMAIL     = os.environ["YOUR_EMAIL"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]
NEWS_TOPICS    = os.environ.get("NEWS_TOPICS", "technology, business, geopolitics, and science")
# ──────────────────────────────────────────────────────────────────────

def get_news_summary():
    client = genai.Client(api_key=GEMINI_API_KEY)
    today = date.today().strftime("%B %d, %Y")

    prompt = f"""Today is {today}. Please search the web and give me a daily news briefing.

Summarize the 7-8 most important news stories from today or the past 24 hours covering: {NEWS_TOPICS}.

For each story:
- Write a clear headline in bold
- Give a 3-4 sentence summary explaining what happened and why it matters
- Note the source

Format it cleanly so it reads like a morning briefing email.
Start with: "Good morning! Here's your news briefing for {today}."
End with a one-line sign-off."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def send_email(summary):
    today = date.today().strftime("%B %d, %Y")
    subject = f"📰 Your Daily News Briefing — {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = YOUR_EMAIL
    msg["To"]      = YOUR_EMAIL

    msg.attach(MIMEText(summary, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(YOUR_EMAIL, GMAIL_APP_PASS)
        server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg.as_string())

    print("✅ Email sent successfully!")


if __name__ == "__main__":
    print("Fetching news summary from Gemini...")
    summary = get_news_summary()
    print("Sending email...")
    send_email(summary)
    print("Done!")
```

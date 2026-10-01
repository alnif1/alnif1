import json
import requests
from bs4 import BeautifulSoup

GITHUB_USER = "alnif1"

def fetch_data():
    url = f"https://github.com/users/{GITHUB_USER}/contributions"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    days = []

    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})

    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(days, f)
    print(f"[+] Contributions fetched: {len(days)} days")

if __name__ == "__main__":
    fetch_data()

import requests
from bs4 import BeautifulSoup
import random

URL = "https://trends24.in/indonesia/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_trending_random():
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # Ambil list trending
    section = soup.find("ol", class_="trend-card__list")
    if not section:
        print("DEBUG: No trend-card__list found")
        return None

    # Ambil semua li
    all_li = section.find_all("li")
    if not all_li:
        print("DEBUG: No <li> found")
        return None
    
    # Pilih random dari list dari 1 - 25
    random_li = random.choice(all_li[:25])
    print("DEBUG: Random <li> found:", random_li)

    tag = random_li.find("a")
    count = random_li.find("span", class_="tweet-count")

    topic = tag.text.strip() if tag else None
    tweets = count.text.strip() if count else "Unknown"

    print(f"DEBUG: RANDOM TOPIC → {topic}, tweets: {tweets}")

    return {
        "topic": topic,
        "tweets": tweets
    }

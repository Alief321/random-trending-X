#!/usr/bin/env python3
"""
Script untuk scrape trending topics dari Indonesia dan update README
Dijalankan oleh GitHub Actions setiap hari
"""

import requests
from bs4 import BeautifulSoup
import random
import re
import textwrap
from datetime import datetime

URL = "https://trends24.in/indonesia/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_trending_random():
    """Ambil satu trending topic secara random dari Indonesia"""
    try:
        res = requests.get(URL, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Ambil list trending
        section = soup.find("ol", class_="trend-card__list")
        if not section:
            print("❌ DEBUG: No trend-card__list found")
            return None

        # Ambil semua li
        all_li = section.find_all("li")
        if not all_li:
            print("❌ DEBUG: No <li> found")
            return None
        
        # Pilih random dari list (max 25 trend pertama)
        random_li = random.choice(all_li[:25])

        tag = random_li.find("a")
        count = random_li.find("span", class_="tweet-count")

        topic = tag.text.strip() if tag else None
        tweets = count.text.strip() if count and count.text.strip() else "Unknown"

        if topic:
            print(f"✅ Random Trending: {topic} ({tweets})")
            return {
                "topic": topic,
                "tweets": tweets,
                "timestamp": datetime.now().isoformat()
            }
        return None

    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return None

def update_readme(trending_data):
    """Update README dengan data trending terbaru"""
    if not trending_data:
        print("❌ Tidak ada data trending, skip update README")
        return False

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        # Format data untuk ditampilkan
        topic = trending_data["topic"].replace("&", "&amp;")
        tweets = trending_data["tweets"]
        timestamp = trending_data["timestamp"]

        # SVG Badge untuk dark mode
        svg_dark = f"""<svg width="500" height="180" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 180">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:#0088ff;stop-opacity:0.05" />
    </linearGradient>
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.15" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#0a0e27" rx="12" stroke="#1a2a4e" stroke-width="1.5" filter="url(#shadow)"/>
  <rect width="100%" height="100%" fill="url(#grad1)" rx="12"/>
  <circle cx="35" cy="35" r="28" fill="#1a3a4a" opacity="0.8"/>
  <text x="35" y="42" text-anchor="middle" font-size="32" dominant-baseline="middle">🔥</text>
  <text x="75" y="28" fill="#00d4ff" font-size="13" font-family="'Segoe UI', Arial, sans-serif" font-weight="600" letter-spacing="0.5">
    RANDOM TRENDING IN INDONESIA TWITTER
  </text>
  <line x1="75" y1="38" x2="480" y2="38" stroke="#1a2a4e" stroke-width="1" opacity="0.5"/>
  <text x="75" y="65" fill="#ffffff" font-size="16" font-family="'Segoe UI', Arial, sans-serif" font-weight="bold">
    <tspan>{topic}</tspan>
  </text>
  <g>
    <svg x="72" y="100" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="#00d4ff" stroke="#00d4ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="12 2 15.09 10.26 24 10.5 17.18 16.34 19.34 24.5 12 18.92 4.66 24.5 6.82 16.34 0 10.5 8.91 10.26 12 2"></polygon>
    </svg>
    <text x="95" y="115" fill="#b0b0b0" font-size="13" font-family="'Segoe UI', Arial, sans-serif">
      {"" if tweets == "Unknown" else tweets}
    </text>
  </g>
  <text x="475" y="175" fill="#b0b0b0" font-size="8" font-family="'Segoe UI', Arial, sans-serif" text-anchor="end" opacity="0.5">
    DARK
  </text>
</svg>"""

        # Simpan SVG ke file terpisah agar bisa di-link dari repo lain
        with open("trending-badge.svg", "w", encoding="utf-8") as svg_file:
            svg_file.write(svg_dark)

        # Buat replacement content dengan marker
        trending_section = (
            f"## 🔥 Today's Random Trending\n\n"
            f"Updated: `{timestamp}`\n\n"
            "### SVG Badge (Dark Mode)\n\n"
            "```html\n"
            f"<a href=\"https://github.com/Alief321/random-trending-X\">\n"
            f"{svg_dark}\n"
            "</a>\n"
            "```\n\n"
            "### Embed Otomatis (link ke file SVG)\n\n"
            "```markdown\n"
            "![Random Trending Indonesia](https://raw.githubusercontent.com/Alief321/random-trending-X/main/trending-badge.svg)\n"
            "```\n\n"
            f"**Trending Topic:** `{topic}`  \n"
            f"**Tweet Count:** {tweets}\n\n"
            "---\n"
        )

        # Cari marker di README (ganti seluruh blok sampai sebelum "## Fitur")
        pattern = r"## 🔥 Today's Random Trending.*?(?=\n## Fitur|\Z)"
        
        trending_section_clean = trending_section.strip() + "\n\n"

        if re.search(pattern, content, re.DOTALL):
            # Replace existing section
            new_content = re.sub(
                pattern,
                trending_section_clean,
                content,
                flags=re.DOTALL
            )
        else:
            # Insert setelah header pertama
            new_content = re.sub(
                r"(# Random Trending X\n\n.*?\n\n)",
                r"\1" + trending_section_clean,
                content,
                flags=re.DOTALL,
                count=1
            )

        # Bersihkan indentasi tak perlu pada heading
        new_content = re.sub(
            r"\n[ \t]+## 🔥 Today's Random Trending",
            "\n## 🔥 Today's Random Trending",
            new_content,
        )

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ README.md updated successfully")
        return True

    except Exception as e:
        print(f"❌ Error updating README: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting trending scraper...")
    trending = get_trending_random()
    if trending:
        update_readme(trending)
        print("✅ Done!")
    else:
        print("❌ Failed to get trending data")

from utils.cache import get_cached_trending
from flask import request

def handler(req):
    trending = get_cached_trending()
    
    # Ambil parameter theme dari query string (default: dark)
    theme = request.args.get('theme', 'dark').lower()
    if theme not in ['light', 'dark']:
        theme = 'dark'

    if not trending:
        topic = "No Data"
        tweets = "0"
    else:
        topic = trending['topic'].replace("&", "&amp;")
        tweets = trending['tweets']

    # Definisi warna untuk setiap tema
    if theme == 'light':
        bg_color = "#ffffff"
        border_color = "#e0e0e0"
        title_color = "#ff6b35"
        topic_color = "#1a1a1a"
        tweets_color = "#666666"
        icon_bg = "#fff3e0"
    else:  # dark
        bg_color = "#0a0e27"
        border_color = "#1a2a4e"
        title_color = "#00d4ff"
        topic_color = "#ffffff"
        tweets_color = "#b0b0b0"
        icon_bg = "#1a3a4a"

    svg = f"""
    <svg width="500" height="160" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 160">
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#{'ff6b35' if theme == 'light' else '00d4ff'};stop-opacity:0.1" />
          <stop offset="100%" style="stop-color:#{'ff9500' if theme == 'light' else '0088ff'};stop-opacity:0.05" />
        </linearGradient>
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.15" />
        </filter>
      </defs>
      
      <!-- Background -->
      <rect width="100%" height="100%" fill="{bg_color}" rx="12" stroke="{border_color}" stroke-width="1.5" filter="url(#shadow)"/>
      
      <!-- Gradient overlay -->
      <rect width="100%" height="100%" fill="url(#grad1)" rx="12"/>
      
      <!-- Icon Background -->
      <circle cx="35" cy="35" r="28" fill="{icon_bg}" opacity="0.8"/>
      
      <!-- Fire Icon (🔥) -->
      <text x="35" y="42" text-anchor="middle" font-size="32" dominant-baseline="middle">🔥</text>
      
      <!-- Title -->
      <text x="75" y="28" fill="{title_color}" font-size="13" font-family="'Segoe UI', Arial, sans-serif" font-weight="600" letter-spacing="0.5">
        RANDOM TRENDING IN INDONESIA TWITTER
      </text>
      
      <!-- Separator line -->
      <line x1="75" y1="38" x2="480" y2="38" stroke="{border_color}" stroke-width="1" opacity="0.5"/>
      
      <!-- Topic -->
      <text x="75" y="65" fill="{topic_color}" font-size="16" font-family="'Segoe UI', Arial, sans-serif" font-weight="bold">
        <tspan>{topic}</tspan>
      </text>
      
      <!-- Tweet count -->
      <g>
        <svg x="72" y="100" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="{title_color}" stroke="{title_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 10.26 24 10.5 17.18 16.34 19.34 24.5 12 18.92 4.66 24.5 6.82 16.34 0 10.5 8.91 10.26 12 2"></polygon>
        </svg>
        <text x="100" y="115" fill="{tweets_color}" font-size="13" font-family="'Segoe UI', Arial, sans-serif">
          {tweets}
        </text>
      </g>
      
      <!-- Theme indicator (small) -->
      <text x="475" y="155" fill="{tweets_color}" font-size="8" font-family="'Segoe UI', Arial, sans-serif" text-anchor="end" opacity="0.5">
      </text>
    </svg>
    """

    from flask import Response
    return Response(svg, mimetype="image/svg+xml")


import time
from .scrape_trending import get_trending_random

CACHE = {
    "data": None,
    "timestamp": 0
}

CACHE_DURATION = 60 * 60 * 24  # 24 jam cache

def get_cached_trending():
    now = time.time()

    # kalau cache masih fresh → langsung return
    if CACHE["data"] and now - CACHE["timestamp"] < CACHE_DURATION:
        return CACHE["data"]

    # kalau cache expired → scrape ulang
    fresh = get_trending_random()
    CACHE["data"] = fresh
    CACHE["timestamp"] = now

    return fresh
    return CACHE["data"]
from flask import Flask, request
from api.trending import handler

app = Flask(__name__)

@app.route("/api/trending")
def trending():
    return handler(request)

# Untuk Vercel

from flask import Flask, Response, request
from api.trending import handler

app = Flask(__name__)

@app.route("/api/trending")
def trending():
    return handler(request)

if __name__ == "__main__":
    app.run(port=3000, debug=True)


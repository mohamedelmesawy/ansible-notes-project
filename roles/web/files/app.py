import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_API_URL = os.getenv("DB_API_URL", "http://127.0.0.1:5001")


@app.route("/")
def index():
    response = requests.get(f"{DB_API_URL}/notes", timeout=5)
    notes = response.json()

    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content", "").strip()

    if content:
        requests.post(
            f"{DB_API_URL}/notes",
            json={"content": content},
            timeout=5
        )

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
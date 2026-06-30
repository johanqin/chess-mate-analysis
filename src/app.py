from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

with open("src/static/mate_data.json") as f:
    MATE_DATA = json.load(f)

@app.route("/api/openings")
def list_openings():
    return jsonify(sorted(MATE_DATA.keys()))

@app.route("/api/mate-squares/<opening>")
def mate_squares(opening):
    return jsonify(MATE_DATA.get(opening, {"white": {}, "black": {}}))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
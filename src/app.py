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
    opening_data = MATE_DATA.get(opening, {})
    result = opening_data.get("all", {"white": {}, "black": {}})
    return jsonify(result)

@app.route("/api/mate-squares/<opening>/<band>")
def mate_squares_by_band(opening, band):
    opening_data = MATE_DATA.get(opening, {})
    result = opening_data.get(band, {"white": {}, "black": {}})
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
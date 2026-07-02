import json
import os
import time
import requests
from flask import Flask, jsonify, render_template
from lichess_fetch import fetch_user_mate_games, aggregate_personal_mate_squares

# Simple in-memory cache: {username_lowercase: (timestamp, result_dict)}
# Avoids re-fetching from Lichess every time the same user is looked up.
PERSONAL_ANALYSIS_CACHE = {}
CACHE_TTL_SECONDS = 60 * 30  # 30 minutes

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

@app.route("/api/mate-squares/<opening>/<band>/<speed>")
def mate_squares_by_band_and_speed(opening, band, speed):
    opening_data = MATE_DATA.get(opening, {})
    speed_data = opening_data.get(speed, {})
    result = speed_data.get(band, {"white": {}, "black": {}})
    return jsonify(result)

@app.route("/api/personal-analysis/<username>")
def personal_analysis(username):
    cache_key = username.lower()
    cached = PERSONAL_ANALYSIS_CACHE.get(cache_key)

    if cached is not None:
        cached_at, cached_result = cached
        if time.time() - cached_at < CACHE_TTL_SECONDS:
            return jsonify(cached_result)

    try:
        parsed_games, total_games_checked = fetch_user_mate_games(username, max_games=500)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"error": "Lichess API error"}), 502
    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not reach Lichess API"}), 502

    if not parsed_games:
        result = {
            "white": {},
            "black": {},
            "total_games": 0,
            "total_games_checked": total_games_checked,
        }
    else:
        result = aggregate_personal_mate_squares(parsed_games, total_games_checked)

    PERSONAL_ANALYSIS_CACHE[cache_key] = (time.time(), result)
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
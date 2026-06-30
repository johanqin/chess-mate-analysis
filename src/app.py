from flask import Flask, jsonify, render_template
from db import DB_PATH
import sqlite3
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

@app.route("/api/mate-squares/<opening>/<int:min_elo>/<int:max_elo>")
def mate_squares_by_rating(opening, min_elo, max_elo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mated_side, mate_square, COUNT(*) as total
        FROM games
        WHERE opening = ?
          AND white_elo BETWEEN ? AND ?
          AND black_elo BETWEEN ? AND ?
        GROUP BY mated_side, mate_square
        ORDER BY mated_side, total DESC
    """, (opening, min_elo, max_elo, min_elo, max_elo))
    rows = cursor.fetchall()
    conn.close()
    
    result = {"white": {}, "black": {}}
    for mated_side, square, count in rows:
        key = "white" if mated_side == "White" else "black"
        result[key][square] = count
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
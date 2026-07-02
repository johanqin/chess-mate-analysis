# Chess Mate Square Analyzer

## Live Post
[I Built a Chess Checkmate Heatmap — Here's What 1.5 Million Games Revealed](https://lichess.org/@/TheMarginalEye/blog/i-built-a-chess-checkmate-heatmap-heres-what-15-million-games-revealed/BO7ljc6r)

A full data pipeline analyzing 1.5 million Lichess checkmate games across 92 named openings to map where kings get mated — broken down by opening choice, rating level, and time control. The database also tracks mating piece, used in the blog post's analysis of which piece delivers the final blow. Includes an interactive heatmap with rating and time control filters, plus a personal lookup that analyzes your own Lichess checkmate history.

## What it does
- Parses PGN/ZST files from the Lichess open database
- Stores checkmate games in a SQLite database
- Analyzes mate square frequency by opening, rating band, and time control
- Applies a minimum sample-size threshold so sparse combinations show "not enough data" instead of a misleading heatmap
- Generates heatmap visualizations
- Fetches and analyzes a Lichess user's own checkmate history via the Lichess API

## Key findings
- The castled square (g1/g8) is the most common mate square across every opening and skill level
- 1.e4 produces 2.5x more checkmates than 1.d4, ending ~4-6 moves earlier
- Queens deliver ~65% of all checkmates regardless of opening family
- In 1.d4, White's queen delivers mate 41.5% of the time at beginner level vs Black's 25% — a gap that nearly vanishes at expert level (33.5% vs 33.2%)
- Opening choice predicts your danger zone. Knowing your opening's heatmap is preparation most players never do.
- Some "prepared" openings — the London System, Catalan, Budapest Defense — have almost no recorded checkmates at beginner level (800-1200), despite being common overall. Cause unconfirmed.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install chess tqdm zstandard matplotlib flask requests
```

## Usage
```bash
python3 src/main.py data/your_file.pgn.zst
python3 src/export_data.py
python3 src/app.py
```

## Personal Lookup
Enter any public Lichess username on the live site to see a heatmap of that account's own checkmate history, pulled live from the Lichess API and cached for 30 minutes.

## Data source
[Lichess open database](https://database.lichess.org)
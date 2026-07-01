# Chess Mate Square Analyzer

## Live Post
[I Built a Chess Checkmate Heatmap — Here's What 1.5 Million Games Revealed](https://lichess.org/@/TheMarginalEye/blog/i-built-a-chess-checkmate-heatmap-heres-what-15-million-games-revealed/BO7ljc6r)

A full data pipeline analyzing 1.5 million Lichess checkmate games across 92 named openings to map where kings get mated — broken down by opening choice, rating level, and mating piece. Includes an interactive heatmap with rating filters.

## What it does
- Parses PGN/ZST files from the Lichess open database
- Stores checkmate games in a SQLite database
- Analyzes mate square frequency by opening and side
- Generates heatmap visualizations

## Key finding
- The castled square (g1/g8) is the most common mate square across every opening and skill level
- 1.e4 produces 2.5x more checkmates than 1.d4, ending ~4-6 moves earlier
- Queens deliver ~65% of all checkmates regardless of opening family
- In 1.d4, White's queen delivers mate 41.5% of the time at beginner level vs Black's 25% — a gap that nearly vanishes at expert level (33.5% vs 33.2%)
- The Italian Game shows a unique pattern: beginners get mated on e8 twice as often as g8, reversing at advanced levels as castling becomes more reliable
- Opening choice predicts your danger zone. Knowing your opening's heatmap is preparation most players never do.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install chess tqdm zstandard matplotlib flask
```

## Usage
```bash
python3 src/main.py data/your_file.pgn.zst
python3 src/visualize.py "Sicilian Defense"
```

## Data source
[Lichess open database](https://database.lichess.org)
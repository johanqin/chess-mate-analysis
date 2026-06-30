# Chess Mate Square Analyzer

A data pipeline that analyzes hundreds of thousands of chess games to find which squares players are most likely to get mated on, broken down by opening.

## What it does
- Parses PGN/ZST files from the Lichess open database
- Stores checkmate games in a SQLite database
- Analyzes mate square frequency by opening and side
- Generates heatmap visualizations

## Key finding
Regardless of opening, both sides are most frequently mated on the same 3 squares — the kingside castled position (g1/g8, h1/h8, f1/f8). The data suggests castle your king, but always maintain escape squares.

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
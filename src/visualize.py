import sys
import chess
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from analyze import get_opening_summary

def draw_heatmap(opening):
    rows = get_opening_summary(opening)

    # Separate Black and White
    black_counts = {r[1]: r[2] for r in rows if r[0] == 'Black'}
    white_counts = {r[1]: r[2] for r in rows if r[0] == 'White'}

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#1a1a1a')
    fig.suptitle(f'Mate Square Heatmap\n{opening}',
                 color='white', fontsize=14, fontweight='bold', y=1.02)

    for ax, counts, title in [
        (axes[0], white_counts, 'White Mated'),
        (axes[1], black_counts, 'Black Mated')
    ]:
        board_data = np.zeros((8, 8))
        for square_name, count in counts.items():
            sq = chess.parse_square(square_name)
            file = chess.square_file(sq)
            rank = chess.square_rank(sq)
            board_data[7 - rank][file] = count

        ax.set_facecolor('#1a1a1a')
        max_val = board_data.max() or 1
        files = 'abcdefgh'

        for rank in range(8):
            for file in range(8):
                value = board_data[rank][file]
                is_light = (rank + file) % 2 == 0
                intensity = value / max_val

                if value > 0:
                    r = int(180 + 75 * intensity)
                    g = int(40 * (1 - intensity))
                    b = int(40 * (1 - intensity))
                    color = f'#{r:02x}{g:02x}{b:02x}'
                else:
                    color = '#f0d9b5' if is_light else '#b58863'

                rect = plt.Rectangle([file, rank], 1, 1, color=color)
                ax.add_patch(rect)

                if value > 0:
                    ax.text(file + 0.5, rank + 0.5, str(int(value)),
                           ha='center', va='center',
                           color='white', fontsize=8, fontweight='bold')

        ax.set_xlim(0, 8)
        ax.set_ylim(0, 8)
        ax.set_xticks([i + 0.5 for i in range(8)])
        ax.set_yticks([i + 0.5 for i in range(8)])
        ax.set_xticklabels(list('abcdefgh'), color='white')
        ax.set_yticklabels([str(i) for i in range(1, 9)], color='white')
        ax.tick_params(colors='white')
        ax.set_title(title, color='white', fontsize=12, pad=10)
        for spine in ax.spines.values():
            spine.set_edgecolor('#444444')

    plt.tight_layout()
    plt.savefig('mate_heatmap.png', dpi=150,
                bbox_inches='tight', facecolor='#1a1a1a')
    print("Saved to mate_heatmap.png")
    plt.show()

if __name__ == "__main__":
    opening = sys.argv[1] if len(sys.argv) > 1 else "Van't Kruijs Opening"
    draw_heatmap(opening)
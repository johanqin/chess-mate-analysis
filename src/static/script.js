async function loadOpenings() {
    const response = await fetch("/api/openings");
    const openings = await response.json();

    const select = document.getElementById("openingSelect");
    openings.forEach(opening => {
        const option = document.createElement("option");
        option.value = opening;
        option.textContent = opening;
        select.appendChild(option);
    });

    loadHeatmap(openings[0]);
}


async function loadHeatmap(opening) {
    const response = await fetch(`/api/mate-squares/${opening}`);
    const data = await response.json();

    drawBoard("whiteBoard", data.white, false);
    drawBoard("blackBoard", data.black, true);
    drawLabels("whiteRankLabels", "whiteFileLabels", false);
    drawLabels("blackRankLabels", "blackFileLabels", true);
}


function drawBoard(boardId, squareCounts, flipped = false) {
    const board = document.getElementById(boardId);
    board.innerHTML = "";

    const maxCount = Math.max(...Object.values(squareCounts), 1);
    const files = "abcdefgh";

    const ranks = flipped ? [1, 2, 3, 4, 5, 6, 7, 8] : [8, 7, 6, 5, 4, 3, 2, 1];
    const fileIndexes = flipped ? [7, 6, 5, 4, 3, 2, 1, 0] : [0, 1, 2, 3, 4, 5, 6, 7];

    for (const rank of ranks) {
        for (const file of fileIndexes) {
            const squareName = files[file] + rank;
            const count = squareCounts[squareName] || 0;
            const intensity = count / maxCount;

            const square = document.createElement("div");
            square.className = "square";
            square.textContent = count > 0 ? count : "";

            const isLight = (rank + file) % 2 === 0;
            const baseColor = isLight ? [240, 217, 181] : [181, 136, 99];

            if (count > 0) {
                const r = Math.round(baseColor[0] + (220 - baseColor[0]) * intensity);
                const g = Math.round(baseColor[1] * (1 - intensity * 0.8));
                const b = Math.round(baseColor[2] * (1 - intensity * 0.8));
                square.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
                square.style.color = intensity > 0.4 ? "white" : "black";
            } else {
                square.style.backgroundColor = `rgb(${baseColor[0]}, ${baseColor[1]}, ${baseColor[2]})`;
                square.style.color = "black";
            }

            board.appendChild(square);
        }
    }
}


function drawLabels(rankLabelsId, fileLabelsId, flipped = false) {
    const rankLabels = document.getElementById(rankLabelsId);
    const fileLabels = document.getElementById(fileLabelsId);
    rankLabels.innerHTML = "";
    fileLabels.innerHTML = "";

    const ranks = flipped ? [1, 2, 3, 4, 5, 6, 7, 8] : [8, 7, 6, 5, 4, 3, 2, 1];
    for (const rank of ranks) {
        const label = document.createElement("div");
        label.className = "label";
        label.textContent = rank;
        rankLabels.appendChild(label);
    }

    const files = flipped ? "hgfedcba" : "abcdefgh";
    for (const char of files) {
        const label = document.createElement("div");
        label.className = "label";
        label.textContent = char;
        fileLabels.appendChild(label);
    }
}


document.getElementById("openingSelect").addEventListener("change", (e) => {
    loadHeatmap(e.target.value);
});

loadOpenings();
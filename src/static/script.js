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
    const ratingValue = document.getElementById("ratingSelect").value;
    const speedValue = document.getElementById("speedSelect").value;

    const url = `/api/mate-squares/${encodeURIComponent(opening)}/${ratingValue}/${speedValue}`;

    const response = await fetch(url);
    const data = await response.json();

    const hasData = Object.keys(data.white).length > 0 || Object.keys(data.black).length > 0;

    if (!hasData) {
        document.getElementById("whiteBoard").innerHTML = "<div style='color:#aaa; font-size:13px; padding:20px; grid-column: span 8;'>Not enough data for this combination</div>";
        document.getElementById("blackBoard").innerHTML = "<div style='color:#aaa; font-size:13px; padding:20px; grid-column: span 8;'>Not enough data for this combination</div>";
        return;
    }

    drawBoard("whiteBoard", data.white, false);
    drawBoard("blackBoard", data.black, true);
    drawLabels("whiteRankLabels", "whiteFileLabels", false);
    drawLabels("blackRankLabels", "blackFileLabels", true);
}


function drawBoard(boardId, squareCounts, flipped = false) {
    const board = document.getElementById(boardId);
    board.innerHTML = "";

    const maxCount = Math.max(...Object.values(squareCounts), 1);
    const totalCount = Object.values(squareCounts).reduce((a, b) => a + b, 0);
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
            const pct = count / totalCount * 100;
            const showColor = pct >= 2;
            const isLight = (rank + file) % 2 === 0;

            if (showColor) {
                let r, g, b;
                if (intensity > 0.6) {
                    r = 220; g = 20; b = 0;
                } else if (intensity > 0.3) {
                    r = 235; g = 120; b = 0;
                } else {
                    r = 245; g = 200; b = 0;
                }
                square.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
                square.style.color = intensity > 0.4 ? "white" : "black";
                square.textContent = Math.round(pct) + "%";
            } else {
                square.style.backgroundColor = isLight ? "rgb(240, 217, 181)" : "rgb(181, 136, 99)";
                square.textContent = "";
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

document.getElementById("ratingSelect").addEventListener("change", () => {
    const opening = document.getElementById("openingSelect").value;
    loadHeatmap(opening);
});

document.getElementById("speedSelect").addEventListener("change", () => {
    const opening = document.getElementById("openingSelect").value;
    loadHeatmap(opening);
});

loadOpenings();
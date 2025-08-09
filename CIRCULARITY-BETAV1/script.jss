const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');

let drawing = false;
let path = [];

const scoreEl = document.getElementById('score');
const bestEl = document.getElementById('best');
let bestScore = sessionStorage.getItem('bestScore') || 0;
bestEl.textContent = `Best: ${bestScore}`;

const drawSound = document.getElementById('drawSound');
const soundToggle = document.getElementById('soundToggle');

canvas.addEventListener('mousedown', e => {
  drawing = true;
  path = [getPos(e)];
  if (soundToggle.checked) {
    drawSound.currentTime = 0;
    drawSound.play();
  }
});

canvas.addEventListener('mousemove', e => {
  if (!drawing) return;
  path.push(getPos(e));
  drawScene();
});

canvas.addEventListener('mouseup', () => {
  drawing = false;
  drawSound.pause();
  evaluate();
});

document.getElementById('clearBtn').addEventListener('click', () => {
  path = [];
  drawScene();
});

document.getElementById('evaluateBtn').addEventListener('click', evaluate);

function getPos(e) {
  const rect = canvas.getBoundingClientRect();
  return { x: e.clientX - rect.left, y: e.clientY - rect.top };
}

function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw center dot
  ctx.fillStyle = 'red';
  ctx.beginPath();
  ctx.arc(canvas.width / 2, canvas.height / 2, 6, 0, Math.PI * 2);
  ctx.fill();

  // Draw path
  if (path.length > 1) {
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(path[0].x, path[0].y);
    path.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.stroke();
  }
}

function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function mean(arr) {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function variance(arr, mu) {
  return arr.reduce((a, b) => a + (b - mu) ** 2, 0) / arr.length;
}

function pointInPolygon(point, polygon) {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i].x, yi = polygon[i].y;
    const xj = polygon[j].x, yj = polygon[j].y;
    const intersect = ((yi > point.y) !== (yj > point.y)) &&
      (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}

function evaluate() {
  const center = { x: canvas.width / 2, y: canvas.height / 2 };
  if (!pointInPolygon(center, path)) {
    scoreEl.textContent = "Red dot not inside loop!";
    return;
  }
  const distances = path.map(p => distance(p, center));
  const mu = mean(distances);
  const std = Math.sqrt(variance(distances, mu));
  const cov = std / mu;
  let score = Math.round(Math.max(0, 100 - cov * 600));
  scoreEl.textContent = `Score: ${score}`;
  if (score > bestScore) {
    bestScore = score;
    sessionStorage.setItem('bestScore', bestScore);
    bestEl.textContent = `Best: ${bestScore}`;
  }
}

drawScene();

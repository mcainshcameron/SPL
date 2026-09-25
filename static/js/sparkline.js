/**
 * SPL v3 — canvas sparklines for market value history (retina-aware).
 * <canvas class="sparkline" width="120" height="44" data-history="[...]"> — rendered on load.
 */
function drawSparkline(canvas, data) {
    if (!data || data.length < 2) return;

    const dpr = window.devicePixelRatio || 1;
    const width = canvas.width, height = canvas.height;   // CSS size (attributes)
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    canvas.width = width * dpr;
    canvas.height = height * dpr;

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    const pad = 3;
    const min = Math.min(...data), max = Math.max(...data);
    const range = max - min || 1;
    const points = data.map((v, i) => ({
        x: pad + (i / (data.length - 1)) * (width - 2 * pad),
        y: height - pad - ((v - min) / range) * (height - 2 * pad)
    }));

    const up = data[data.length - 1] >= data[0];
    const color = up ? '52, 211, 153' : '255, 92, 92';

    const grad = ctx.createLinearGradient(0, 0, 0, height);
    grad.addColorStop(0, 'rgba(' + color + ', 0.28)');
    grad.addColorStop(1, 'rgba(' + color + ', 0)');
    ctx.beginPath();
    ctx.moveTo(points[0].x, height);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, height);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    points.forEach((p, i) => (i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y)));
    ctx.strokeStyle = 'rgb(' + color + ')';
    ctx.lineWidth = 1.8;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.stroke();

    const last = points[points.length - 1];
    ctx.beginPath();
    ctx.arc(last.x, last.y, 2.6, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgb(' + color + ')';
    ctx.fill();
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.sparkline[data-history]').forEach(canvas => {
        try {
            drawSparkline(canvas, JSON.parse(canvas.dataset.history));
        } catch (e) {
            console.error('Error rendering sparkline:', e);
        }
    });
});

window.drawSparkline = drawSparkline;

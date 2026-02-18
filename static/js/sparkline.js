/**
 * SPL v2 - Sparkline Chart Renderer
 * Lightweight canvas-based sparklines for market value history
 */

function drawSparkline(canvas, data) {
    if (!data || data.length === 0) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const padding = 2;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Calculate min/max for scaling
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1; // Prevent division by zero
    
    // Scale data points to canvas
    const points = data.map((value, index) => {
        const x = padding + (index / (data.length - 1)) * (width - 2 * padding);
        const y = height - padding - ((value - min) / range) * (height - 2 * padding);
        return { x, y };
    });
    
    // Determine color based on trend
    const firstValue = data[0];
    const lastValue = data[data.length - 1];
    const isPositive = lastValue >= firstValue;
    const lineColor = isPositive ? 'rgba(16, 185, 129, 1)' : 'rgba(239, 68, 68, 1)';
    const fillColor = isPositive ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)';
    
    // Draw filled area
    ctx.beginPath();
    ctx.moveTo(points[0].x, height - padding);
    points.forEach((point, index) => {
        if (index === 0) {
            ctx.lineTo(point.x, point.y);
        } else {
            ctx.lineTo(point.x, point.y);
        }
    });
    ctx.lineTo(points[points.length - 1].x, height - padding);
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    
    // Draw line
    ctx.beginPath();
    points.forEach((point, index) => {
        if (index === 0) {
            ctx.moveTo(point.x, point.y);
        } else {
            ctx.lineTo(point.x, point.y);
        }
    });
    ctx.strokeStyle = lineColor;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.stroke();
    
    // Draw point at the end
    const lastPoint = points[points.length - 1];
    ctx.beginPath();
    ctx.arc(lastPoint.x, lastPoint.y, 3, 0, 2 * Math.PI);
    ctx.fillStyle = lineColor;
    ctx.fill();
}

// Auto-render sparklines on page load
document.addEventListener('DOMContentLoaded', function() {
    const sparklines = document.querySelectorAll('.sparkline[data-history]');
    sparklines.forEach(canvas => {
        try {
            const history = JSON.parse(canvas.dataset.history);
            drawSparkline(canvas, history);
        } catch (e) {
            console.error('Error rendering sparkline:', e);
        }
    });
});

// Export for use in other scripts
window.drawSparkline = drawSparkline;

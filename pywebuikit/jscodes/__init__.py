create_2DCanvas = """\
cv = document.createElement("canvas");
ctx = cv.getContext("2d");
let resize_task = false;

cv.className = "main-canvas";
document.body.appendChild(cv);

createCanvas2DHook = (method, hook) => {
    let rawFunc = CanvasRenderingContext2D.prototype[method];
    CanvasRenderingContext2D.prototype[method] = function(...args) {
        return hook(this, rawFunc, ...args);
    }
}

createCanvas2DMethod = (method, func) => {
    CanvasRenderingContext2D.prototype[method] = func;
}

resizeCanvas = () => {
    cv.width = window.innerWidth;
    cv.height = window.innerHeight;
    ctx.reset();
};

resizeCanvas();
window.addEventListener("resize", resizeCanvas);
"""

c2d_extend = """\
// createCanvas2DHook('drawImage', (t, f, ...args) => {
//     if (t.globalAlpha != 0.0) return f(...args);
// });
"""
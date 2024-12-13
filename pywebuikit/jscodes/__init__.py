CREATE_2DCANVAS = """\
cv = document.createElement("canvas");
ctx = cv.getContext("2d");

cv.className = "main-canvas";
document.body.appendChild(cv);

let resize_task = false;

resizeCanvas = () => {
    cv.width = window.innerWidth;
    cv.height = window.innerHeight;
    ctx.reset();
};

resizeCanvas();
window.addEventListener("resize", resizeCanvas);
"""
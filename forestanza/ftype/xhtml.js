function storePos() {
    var doc = document.documentElement;
    var y = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop  || 0);
    var h = (document.height || document.body.offsetHeight);
    var pos = y / h;
    localStorage.setItem('scrollRelPos', pos);
}

function loadPos() {
    var pos = localStorage.getItem('scrollRelPos') || 0;
    var h = (document.height || document.body.offsetHeight);
    var y = pos * h;
    window.scrollTo(0, y);
}

function updatePos() {
    doUpdatePos = true;
    storePos();
}

function onResizePost() { loadPos(); }
function onResize() {
    if (this.resizeTimeout) { clearTimeout(this.resizeTimeout); }
    this.resizeTimeout = setTimeout(onResizePost, 500);
}
function onScroll() {
    if (doUpdatePos) {
        doUpdatePos = false;
        if (this.scrollTimeout) {
            clearTimeout(this.scrollTimeout);
            this.scrollTimeout = null;
        }
        this.scrollTimeout = setTimeout(updatePos, 500);
    }
}

(function () {  // Main
    var doUpdatePos = true;
    window.onload = function () { loadPos(); };
    window.onbeforeunload = function (e) { storePos(); };
    window.onresize = onResize;
    window.onscroll = onScroll;
})();

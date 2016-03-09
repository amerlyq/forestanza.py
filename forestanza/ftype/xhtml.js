function storePos() {
    var doc = document.documentElement;
    var y = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop  || 0);
    var h = (document.height || document.body.offsetHeight);
    var pos = y / h;
    localStorage.setItem('scrollRelPos', pos);
}

function loadPos() {
    var pos = localStorage.getItem('scrollRelPos');
    if (typeof pos == 'undefined') { return; }
    var h = (document.height || document.body.offsetHeight);
    var y = Math.round(pos * h);
    window.scrollTo(0, y);
}

function onScroll() {
    if (this.scrollTimeout) { clearTimeout(this.scrollTimeout); }
    this.scrollTimeout = setTimeout(storePos, 500);
}

(function () {  // Main
    window.onresize = loadPos;
    window.onscroll = onScroll;
})();

function storePos() {
    var doc = document.documentElement;
    var y = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop  || 0);
    var h = (document.height || document.body.offsetHeight);
    var pos = y / h;
    sessionStorage.setItem('scrollRelPos', pos);
}

function loadPos() {
    var pos = sessionStorage.getItem('scrollRelPos');
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
    window.onbeforeunload = storePos;
    window.onresize = loadPos;
    window.onscroll = onScroll;
})();

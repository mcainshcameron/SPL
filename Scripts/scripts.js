window.addEventListener('load', function() {
    const lionLogo = document.getElementById("lion-logo");
    if (typeof truncatedLionLogo !== 'undefined') {
        lionLogo.src = truncatedLionLogo;
    } else {
        console.error("truncatedLionLogo is not defined. Make sure modified_lion.js is loaded.");
    }
});

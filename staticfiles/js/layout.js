$(document).ready(function () {
    // Initialize Feather
    feather.replace();

    // Set Active Menu Item
    var CURRENT_URI = window.location.pathname.
        split('#')[0].split('?')[0];
    $(".sidebar").find('a[href="' + CURRENT_URI + '"]').addClass('active');
});
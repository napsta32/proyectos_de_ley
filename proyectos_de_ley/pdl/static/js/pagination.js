$(document).ready(function () {
    // to fade in on page load
    $('a[rel="page"]').click(function (e) {
        redirect = $(this).attr('href');
        e.preventDefault();
        $('html, body').animate({ scrollTop: 0 }, 0, function () {});
        $('#contenido').fadeOut(400, function() {});
        document.location.href = redirect;
        $('#contenido').fadeIn(900, function() {});
    });
})
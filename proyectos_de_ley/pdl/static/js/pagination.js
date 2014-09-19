$(document).ready(function () {
    // to fade in on page load
    $('a[rel="page"]').click(function (e) {
        redirect = $(this).attr('href');
        e.preventDefault();
        $('#contenido').fadeOut(400, function() {
            document.location.href = redirect;
        });
        $('html, body').animate({ scrollTop: 0 }, 0);
        $('#contenido').fadeIn(1000, function() {});
    });
})
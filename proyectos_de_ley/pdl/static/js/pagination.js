$(document).ready(function(){
    // to fade in on page load
    $("#contenido").fadeIn(400);
    // to fade out before redirect
    $('a[rel="page"]').click(function(e){
        redirect = $(this).attr('href');
        e.preventDefault();
        $('#contenido').fadeOut(400, function(){
            document.location.href = redirect
        });
    });
})
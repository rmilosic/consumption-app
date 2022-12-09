$(document).ready( function() {

    
    $(".load-btn").on("click", function() {
        
        // $(".visually-hidden").removeClass("visually-hidden")
        // $(".hideText").text("")

        $(this).html('<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true">'+
        '</span><span class=""> Nalagam </span>')
    })
    
    var url = window.location.pathname;
    $('ul#admin_nav a[href="' + url + '"]').addClass('active');
    // $('ul#navigation a').filter(function() {
    //     return this.href == url;
    // }).parent().addClass('active');
})

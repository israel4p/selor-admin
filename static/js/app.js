$(document).ready(function() {
    $('.delete').click(function() {
        $('.notification').hide();
    });

    $('.submit').click(function() {
        $('.submit').attr('disabled', true)
    });

});

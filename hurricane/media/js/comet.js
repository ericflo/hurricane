$(function() {
    var on_success = function(response) {
        $('.items').prepend('<li>' + response + '</li>');
        ajax_request();
    };
    
    var on_error = function(response) {
        setTimeout(ajax_request, 500);
    };
    
    var ajax_request = function() {
        $.ajax({url: '/comet/', type: 'POST', dataType: 'text', success: on_success, error: on_error});
    };
    
    ajax_request();
});

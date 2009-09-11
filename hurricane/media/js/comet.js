$(function() {
    var ajax_request = function() {
        $.ajax({url: '/comet/', type: 'POST', dataType: 'text', success: on_success, error: on_error});
    };
    
    var on_success = function(response) {
        $('body').append(response);
        ajax_request();
    };
    var on_error = function(response) {
        alert(response);
        ajax_request();
    };
    
    ajax_request();
});

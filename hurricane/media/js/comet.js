$(function() {
    var on_success = function(response) {
        
    };
    var on_error = function(response) {
        
    };
    $.ajax(url: '/comet/', type: 'POST', dataType: 'text', success: on_success, error: on_error);
});
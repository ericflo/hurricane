$(function() {
    var cursor = null;
    
    var on_success = function(response) {
        $('body').append(response + '<br><br>');
        var messages = JSON.parse(response).messages;
        cursor = messages[messages.length-1].id;
        /*ajax_request();*/
        setTimeout(ajax_request, 2000);
    };
    
    var on_error = function(response) {
        setTimeout(ajax_request, 500);
    };
    
    var ajax_request = function() {
        var args = {'cursor': cursor};
        $.ajax({url: '/comet/', type: 'POST', dataType: 'text', data: $.param(args), success: on_success, error: on_error});
    };
    
    ajax_request();
});

$(function() {
    var cursor = null;
    
    var on_success = function(response) {
        var messages = JSON.parse(response).messages;
        cursor = messages[messages.length-1].id;
        /*ajax_request();*/
        for(var msg_idx in messages) {
            var msg = messages[msg_idx];
            var json_msg = JSON.stringify(msg);
            $('.items').prepend('<li>' + json_msg + '</li>');
        }
        ajax_request();
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

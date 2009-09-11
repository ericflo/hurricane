/* blah */
$(function() {
    Hurricane.add_callback('random', function(msg) {
        var json_msg = JSON.stringify(msg);
        $('.items').prepend('<li>' + json_msg + '</li>');

        if ($('.items li').length > 200) {
            $('.items li:last').remove();
        }
    });
});
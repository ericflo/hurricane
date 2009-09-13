$(function() {
    
    var msg_form = $('#send-msg');
    /* Pretty sure you have to do this kind of crap for IE */
    if(msg_form.length > 0) {
        msg_form.submit(function() {
            var msg = $('input[type="text"]', this).val();
            $.ajax({
                url: '/comet/',
                type: 'POST',
                data: JSON.stringify({'msg': msg})
            });
            $('input[type="text"]', this).val('');
            return false;
        });
    }
    
    function callback(data) {
        var msg = data.raw_data;
        $('<li><div class="user"><a href="#">' + data.user_data.username + '</a></div><span>' + msg.msg + '</span><div class="clear"></div></li>').insertAfter('#messages h2');
        if ($('#messages li').length > 200) {
            $('#messages li:last').remove();
        }
    }

    Hurricane.add_callback('hubbub', callback);
});
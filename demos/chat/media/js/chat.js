$(function() {

    function callback(data) {
        var msg = data.raw_data;


    }

    Hurricane.add_callback('chat', callback);

    $('#chat-input').submit(function () {
        var data = $('#message').val();
        $.ajax({
            url: '/comet/',
            method: 'POST',
            data: data
        });
        return false;
    });
});
$(function() {

    function callback(data) {
        var msg = data.raw_data;


    }

    Hurricane.add_callback('chat', callback);

    $('#chat-input').submit(function () {
        var data = $('#message').val();
        $.ajax({
            url: '/comet/',
            type: 'POST',
            data: JSON.stringify({'message': data})
        });
        return false;
    });
});
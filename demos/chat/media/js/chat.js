$(function() {

    function callback(data) {
        var msg = data.raw_data;


    }

    Hurricane.add_callback('chat', callback);

    $('#chat-input').submit(function () {
        var data = $('#message').value()
        $.ajax({

        })
    });
});
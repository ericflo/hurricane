$(function() {

    function callback(data) {
        var msg = data.raw_data;
        $('.items').prepend('<li>' + msg.message + '</li>');
    }

    Hurricane.add_callback('comet', callback);

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
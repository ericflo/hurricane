$(function() {
    var nick = null;

    function callback(data) {
        var msg = data.raw_data;
        $('.items').prepend('<li>' + msg.nick + ': ' + msg.message + '</li>');
    }

    Hurricane.add_callback('comet', callback);

    $('#chat-input').submit(function () {
        var data = $('#message').val();
        $.ajax({
            url: '/comet/',
            type: 'POST',
            data: JSON.stringify({'message': data, 'nick': nick})
        });
        return false;
    });

    $('#nick').click(function() {
        var name = prompt("What's your name?", "");
        nick = name;
        return false;
    });
});
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
<<<<<<< HEAD
            data: JSON.stringify({'message': data})
        })
=======
            data: data
        });
        return false;
>>>>>>> f5b7e4cdb430a29734c71d6725a355ec97fe7bed
    });
});
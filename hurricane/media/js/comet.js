var Hurricane = (function() {
    Hurricane = function() {
        var hurricane = this;

        this.cursor = null;
        this.initial_backoff = 500;
        this.backoff_iteration = 1;
        this.url = '/comet/';
        setTimeout(function() {
            hurricane.ajax_request();
        }, 50); /* Probably should have a better way to start the first request */
    };

    Hurricane.prototype = {
        on_success: function(response) {
            var messages = JSON.parse(response).messages;
            this.cursor = messages[messages.length-1].id;
            for (var msg_idx in messages) {
                /* TODO: Make this dispatch */
                var msg = messages[msg_idx];
                var json_msg = JSON.stringify(msg);
                $('.items').prepend('<li>' + json_msg + '</li>');

                if ($('.items li').length > 200) {
                    $('.items li:last').remove();
                }
            }
            this.backoff_iteration = 1;
            this.ajax_request();
        },

        on_error: function(response) {
            setTimeout(function() {
                hurricane.ajax_request();
            }, this.backoff_iteration * this.initial_backoff);
        },

        ajax_request: function() {
            var args = $.param({'cursor': this.cursor});
            $.ajax({url: this.url, type: 'POST', dataType: 'text', data: args, success: this.on_success, error: this.on_error});
        }
    }

    return new Hurricane();
})();
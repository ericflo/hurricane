var Hurricane = (function() {
    Hurricane = function() {        
        this.cursor = null;
        this.initial_backoff = 500;
        this.backoff_iteration = 1;
        this.url = '/comet/';
        this.ajax_request();
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
                this.ajax_request();
            }, this.backoff_iteration * this.initial_backoff);
        },

        ajax_request: function() {
            var args = $.param({'cursor': this.cursor});
            var hurricane = this;
            $.ajax({
                url: this.url,
                type: 'POST',
                dataType: 'text',
                data: args, success: function(response) {
                    hurricane.on_success(response);
                },
                error: function(response) { 
                    hurricane.on_error(response);
                }
            });
        }
    };
    
    return new Hurricane();
})();
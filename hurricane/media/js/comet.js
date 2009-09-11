var Hurricane = (function() {
    Hurricane = function() {        
        this.cursor = null;
        this.initial_backoff = 500;
        this.backoff_iteration = 1;
        this.url = '/comet/';
        this.ajax_request();
        this.callbacks = {};
    };

    Hurricane.prototype = {
        on_success: function(response) {
            var messages = JSON.parse(response).messages;
            this.cursor = messages[messages.length-1].id;
            for (var msg_idx in messages) {
                var msg = messages[msg_idx];
                var callback = this.callbacks[msg.kind];
                if(callback) {
                    callback(msg);
                }
            }
            this.backoff_iteration = 1;
            this.ajax_request();
        },

        on_error: function(response) {
            var hurricane = this;
            setTimeout(function() {
                hurricane.ajax_request();
            }, hurricane.backoff_iteration * hurricane.initial_backoff);
        },

        ajax_request: function() {
            var args = $.param({'cursor': this.cursor});
            var hurricane = this;
            $.ajax({
                url: this.url,
                type: 'POST',
                dataType: 'text',
                data: args,
                success: function(response) {
                    hurricane.on_success(response);
                },
                error: function(response) { 
                    hurricane.on_error(response);
                }
            });
        },
        
        add_callback: function(kind, callback) {
            this.callbacks[kind] = callback;
        }
    };
    
    return new Hurricane();
})();
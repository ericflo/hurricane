$(function() {
    function escape_html(html) {
        return html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\"/g, '&quot;').replace(/'/g, '&#39;');
    }
    
    function linkify(msg) {
        var matches = msg.match(/https?:\/\/\S+/g);
        if (!matches) {
            return msg;
        }

        while (matches.length > 0) {
            var url = matches.shift();
            msg = msg.replace(url, '<a target="_blank" href="' + url + '">' + url + '</a>');
        }
        return msg;
    }

    function twitterfy(msg) {
        var matches = msg.match(/@[a-zA-Z0-9_]+/g);
        if (!matches) {
            return msg;
        }

        while (matches.length > 0) {
            var user = matches.shift();
            msg = msg.replace(user, '<a target="_blank" href="http://twitter.com/' + user.substring(1) + '">' + user + '</a>');
        }
        return msg;
    }

    function hashify(msg) {
        var matches = msg.match(/ #[a-zA-Z0-9]{2,}/g);
        if (!matches) {
            return msg;
        }

        while (matches.length > 0) {
            var hash_tag = matches.shift();
            msg = msg.replace(hash_tag, '<a target="_blank" href="http://twitter.com/#search?q=' + hash_tag.substring(1) + '">' + hash_tag + '</a>');
        }
        return msg;
    }
    
    function add_item(html, initial) {
        $('.items').prepend(html);
        $('.new_item').each(function() {
            $(".timeago", this).timeago();
            if (!initial) {
                $(this).fadeIn("slow");
            }
            $(this).removeClass('new_item');
        });
        if ($('.items li').length > 200) {
            $('.items li:last').remove();
        }
        $('#ajax-loader').remove();
    }
    
    var filters = [linkify, twitterfy, hashify];
    
    Hurricane.add_callback('random', function(msg) {
        var body = escape_html(tweet.text);
        for (var i in filters) {
            body = filters[i].call(this, body);
        }
        add_item('<li class="new_item"><div class="line clearfix"><img src="' + tweet.user.profile_image_url
            + '" width="40" height="40"></img> <strong>(by <a target="_blank" '
            + 'href="http://twitter.com/' + tweet.user.screen_name + '">'
            + tweet.user.screen_name + '</a>)</strong> ' + body
            + ' -- <a href="http://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id + '" target="_blank"><abbr class="timeago" title="' + tweet.iso8601 + '">' + tweet.iso8601 + '</abbr></a></div></li>',
            initial);
        
        var json_msg = JSON.stringify(msg);
        $('.items').prepend('<li>' + json_msg + '</li>');

        if ($('.items li').length > 200) {
            $('.items li:last').remove();
        }
    });
});
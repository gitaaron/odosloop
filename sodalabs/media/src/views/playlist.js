define(['exports', 'underscore', 'backbone', 'template', './song'], function(exports, _, Backbone, template, song_view) {
    return Backbone.View.extend({

        el:$('.playlist_container'),

        initialize:function() {
            this.collection.on('add', this.appendSong, this);
        },

        appendSong:function(song) {
            var el = $(template.playlist_item_tpl(song.attributes));
            this.$('#track_list').append(el);
            new song_view({el:el, model:song});
        },

    });

});

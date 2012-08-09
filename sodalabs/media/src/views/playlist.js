define(['exports', 'underscore', 'backbone', 'template', './song'], function(exports, _, Backbone, template, song_view) {
    return Backbone.View.extend({

        el:$('.playlist_container'),

        initialize:function() {
            this.collection.on('add', this.appendSong, this);
            this.collection.on('loading', this.loading, this);
            this.collection.on('new_list', this.new_list, this);
        },

        appendSong:function(song) {
            var el = $(template.playlist_item_tpl(song.attributes));
            this.$('#track_list').append(el);
            new song_view({el:el, model:song});
        },

        loading:function(){
            this.$('#playlist_title').html('keep your pants on...');
            this.$('#track_list').html('');
        },

        new_list:function(data) {
            this.$('#playlist_title').html(data.title);
        }


    });

});

define(['exports', 'underscore', 'backbone', 'template'], function(exports, _, Backbone, template) {
    exports.Playlist = Backbone.View.extend({
        el:$('.playlist_container'),

        initialize:function() {
            console.log('listen to add');
            this.collection.on('add', this.appendSong, this);
        },

        appendSong:function(song) {


            this.$('#track_list').append(template.playlist_item_tpl());
        }


    });

});

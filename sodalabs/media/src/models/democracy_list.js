define(['underscore','backbone', './song'], function(_, Backbone, song) {

    return Backbone.Collection.extend({
        url:'/api/democracy_list',
        model:song,
        initialize:function(options) {
            this.app = options.app;
        },
        selectSong:function(song) {
            this.app.navigate('song');
        }
    });


});

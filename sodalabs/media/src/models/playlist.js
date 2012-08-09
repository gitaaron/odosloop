define(['underscore','backbone', './song'], function(_, Backbone, song) {

    return Backbone.Collection.extend({
        url:'/api/democracy_list',
        model:song,
        currentSong:null,
        initialize:function(options) {
            this.app = options.app;
        },
           
        selectSong:function(song) {
            this.currentSong = song;
            this.app.navigate('song');
        },

        goToNext:function() {
            var index = this.indexOf(this.currentSong);
            var song = this.models[index+1];
            song.trigger('play');
        },

        loadSearch:function(q) {
            var self = this;
            $.get('/api/search', {'q':unescape(q)}, function(data) {
                console.log('search results : ' + data);
                data = JSON.parse(data);
                self.add(data);
            });        
        }

    });


});

require.config({
    paths:{
        jade:'../lib/jade',
        backbone:'../lib/backbone',
        bootstrap:'../bootstrap/js/bootstrap.min',
        underscore:'../lib/underscore'
    }
});

/* Global event sender */
var vent;

require(['jquery', 'underscore', 'backbone', 'bootstrap', 'models/playlist', 'models/song', 'views/playlist', 'views/search'], function($, _und, Backbone, bootstrap, playlist, song, playlist_view, search_view) {

    vent = _.extend({}, Backbone.Events);

    var Workspace = Backbone.Router.extend({
        routes: {
            'test':'test',
            'song':'song'
        },
        test:function() {
            console.log('this is a test');
        },
        song:function() {
            console.log('this is a song');
        }
    });

    $(function() {

        var wp = new Workspace();
        Backbone.history.start();
        var pl = new playlist({app:wp});
        new playlist_view({collection:pl});
        pl.add([{name:'Kids', artist:'MGMT'}, {name:'Far Nearer', artist:'Jamie xx'}]);
        
        vent.bind('goToNext', function() {
            pl.goToNext();
        });

        var s = new search_view();
        s.bind('search', function(data) {
            console.log('search : ' + data.q);
            pl.loadSearch(data.q);
        }, this);   

    });

});

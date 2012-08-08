require.config({
    paths:{
        jade:'../lib/jade',
        backbone:'../lib/backbone',
        bootstrap:'../bootstrap/js/bootstrap.min',
        underscore:'../lib/underscore'
    }
});

require(['jquery', 'underscore', 'backbone', 'bootstrap', 'models/democracy_list', 'models/song', 'views/playlist'], function($, _, Backbone, bootstrap, democracy_list, song, playlist_view) {


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
        var dl = new democracy_list({app:wp});
        new playlist_view({collection:dl});
        dl.add([{name:'Kids', artist:'MGMT'}, {name:'Far Nearer', artist:'Jamie xx'}]);
    });

});

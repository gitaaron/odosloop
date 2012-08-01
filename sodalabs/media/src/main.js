require.config({
    paths:{
        jade:'../lib/jade',
        backbone:'../lib/backbone',
        bootstrap:'../bootstrap/js/bootstrap.min',
        underscore:'../lib/underscore'
    }
});

require(['jquery', 'underscore', 'backbone', 'bootstrap', 'models', 'views'], function($, _, Backbone, bootstrap, models, views) {

    $(function() {
        var democracy_list = new models.DemocracyList();
        new views.Playlist({collection:democracy_list});
        democracy_list.add([{name:'asdf'}, {name:'feqfq'}]);
    });

});

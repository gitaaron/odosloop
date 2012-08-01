define(['exports', 'underscore', 'backbone'], function(exports, _, Backbone) {

    exports.Song = Backbone.Model.extend({
        url:'/api/song'
    });

    exports.DemocracyList = Backbone.Collection.extend({
        url:'/api/democracy_list',
        model:this.Song
    });
});

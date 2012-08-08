define(['underscore','backbone'], function(_, Backbone) {
    return Backbone.Model.extend({
        url:function(song) { return '/jukebox/get_closest_video?artist='+this.attributes.artist+'&name='+this.attributes.name},
        select : function() {
            var self = this;
            this.fetch({
                success:function(response) {
                    self.trigger('fetch_success');
                },
                error:function(response) {
                    alert('An error occurred trying to fetch the closest match'); 
                }
            });
            this.collection.selectSong(this);
        }
    });

});

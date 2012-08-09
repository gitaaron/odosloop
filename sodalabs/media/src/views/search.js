define(['underscore', 'backbone'], function(_und, backbone) {
    return Backbone.View.extend({
        el:$('#music_search_form'),

        initialize:function() {
            var i = this.$('input');
            i.bind('click', function(e) {
                if(i.attr('value')=='Search Music') {
                    i.attr('value', '');
                }
            });

            var self = this;

            $(this.el).submit(function() {
                self.trigger('search', {q:i.attr('value')});
                console.log('submit');
                return false;
            });
        }
    
    });
});

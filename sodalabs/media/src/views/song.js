define(['underscore', 'backbone', '../youtube_player'], function(_, Backbone, youtube_player) {

    API_KEY = 'AI39si4G2-0d2C5E98vAfsM8RT5Z7h8md7wClPvY_Jhfu8oyonkYkjCuA_DBJehHGtPzb6UdIspQhf7M3Cc6_NW2pTT3t4uZ4A';

    var app; 

    return Backbone.View.extend({
        initialize:function() {
            this.model.on('fetch_success', function() {
                var s = this.model.attributes;
                var t = 'odosloop - ' + s['artist'] + ' - ' + s['name'];

                try {
                    $('#browser_title').html(t);
                } catch(err) { 
                    document.title = t; 
                }

                vent.on('playing:'+s['video_id'], function() {
                    $('.now_playing').removeClass('now_playing');
                    $(this.el).addClass('now_playing');
                }, this);
                youtube_player.play(s['video_id'], s['video_title']);

            }, this);

            this.model.on('play', this.selectSong, this);

        },

        events:{
            'click .song':'selectSong'
        },

        selectSong:function() {
            // show loading div
            $('#youtube_container').hide();
            $('#loadingVideoDiv').show();
            $('#youtube_container').html('<h3 id="title"></h3><div id="videoDiv"></div>');
            this.model.select();
        }


    });

});

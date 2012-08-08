define(['underscore', 'backbone'], function(_, Backbone) {

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

                this.play(s['video_id'], s['video_title']);

            }, this);
        },
        events:{
            'click .song':'selectSong'
        },

        selectSong:function(e) {
            this.model.select();
        },

        play : function(video_id, video_title) {
            console.log('play : ' + video_id);
            $('#title').html(video_title);
            $(this.el).addClass('now_playing');
            // hide loading div and show video container
            $('#youtube_container').css('display','block');
            $('#loadingVideoDiv').css('display','none');


            // Lets Flash from another domain call JavaScript
            var params = { allowScriptAccess: "always" , height:200, width:350, wmode:'opaque'};
            // The element id of the Flash embed
            var atts = { id: "ytPlayer" , 'wmode':'opaque'};
            // All of the magic handled by SWFObject (http://code.google.com/p/swfobject/)
            swfobject.embedSWF("http://www.youtube.com/v/" + video_id + "&version=3&enablejsapi=1&playerapiid="+API_KEY,
                               "videoDiv", "350", "200", "8", null, null, params, atts);




        }

    });

});


function onYouTubePlayerReady(playerId) {
    console.log('onYouTubePlayer');
    ytplayer = document.getElementById('ytPlayer');
    ytplayer.addEventListener('onStateChange','Playlist.onPlayerStateChange');
    ytplayer.addEventListener('onError','Playlist.onPlayerError');
    ytplayer.playVideo();
}




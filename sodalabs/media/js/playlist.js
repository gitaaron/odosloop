API_KEY = 'AI39si4G2-0d2C5E98vAfsM8RT5Z7h8md7wClPvY_Jhfu8oyonkYkjCuA_DBJehHGtPzb6UdIspQhf7M3Cc6_NW2pTT3t4uZ4A';

function onYouTubePlayerReady(playerId) {
    ytplayer = document.getElementById('ytPlayer');
    ytplayer.addEventListener('onStateChange','Playlist.onPlayerStateChange');
    ytplayer.addEventListener('onError','Playlist.onPlayerError');
    ytplayer.playVideo();
    Playlist.player = ytplayer;
}

var Playlist = {
    songs : new Array(),
    currentSong : false,
    player : false,

    open : function(songId) {
        songId = parseInt(songId);
        song = Playlist.songs[songId];

        Playlist.currentSong = songId;
        $.get('/jukebox/open/', song, function(data) {
                jsonData = JSON.parse(data);
                if(jsonData['status']=='ok') {
                    Playlist.play(jsonData['video_id'], jsonData['video_title']);
                    $('#radio_form').css('display','block');
                    track = $('#radio_form').children().filter('input[name|=lastfm_track]');
                    track.attr('value',jsonData['lastfm_track_id'])
                    console.log('track : ' + track.attr('id'));
                } else { 
                    Playlist.markSongAsErred(songId);
                    Playlist.goToNext();
                }
        });
        return false;
    },

    markSongAsErred : function(songId) {
        elem = Playlist.getElemById(songId);
        elem.html('(error) ' + elem.html());
    },

    play : function(id,title) {
        /*
        * Simple player embed
        */
        songId = Playlist.currentSong;
        $('.recent_song').attr('class','recent_song');
        elem = Playlist.getElemById(songId);
        $(elem).attr('class','recent_song now_playing');
        $('#title').html(title);
        if(Playlist.player) {
            Playlist.player.loadVideoById(id);
        } else {
            // The video to load.
            var videoID = id
            // Lets Flash from another domain call JavaScript
            var params = { allowScriptAccess: "always" };
            // The element id of the Flash embed
            var atts = { id: "ytPlayer" };
            // All of the magic handled by SWFObject (http://code.google.com/p/swfobject/)
            swfobject.embedSWF("http://www.youtube.com/v/" + videoID + "&enablejsapi=1&playerapiid="+API_KEY,
                               "videoDiv", "480", "295", "8", null, null, params, atts);

        }


    },

    getElemById : function(id) {
        return $('#'+id);
    },

    onPlayerStateChange : function(state) {
        if (state==0) {
            Playlist.goToNext();
        }
    },

    onPlayerError : function(code) {
        Playlist.goToNext();
    },
    
    goToNext : function() {
        songId = Playlist.currentSong+1;
        Playlist.open(songId);
    }

}

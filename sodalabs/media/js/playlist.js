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
    lastSongLogged : false,
    player : false,
    
    saveSongAsPlayed : function(songId,lastFMTrackSongId) {
        if(songId == Playlist.currentSong && songId != Playlist.lastSongLogged) {
            $.post('/accounts/song_played/' + lastFMTrackSongId+'/', function(data) {
                    jsonData = JSON.parse(data);
                    if(jsonData['status']=='ok') {
                        console.log('song_played result success');
                        Playlist.lastSongLogged = songId;
                    } else { 
                        console.log('song_played result failed because : ' + jsonData['message']);
                    }
            });
        } 
    },

    open : function(songId) {
        songId = parseInt(songId);
        song = Playlist.songs[songId];

        Playlist.currentSong = songId;
        $.get('/jukebox/open/', song, function(data) {
                jsonData = JSON.parse(data);
                if(jsonData['status']=='ok') {
                    Playlist.play(jsonData['video_id'], jsonData['video_title']);
                    // set radio form
                    $('#radio_form').css('display','block');
                    radio_track = $('#radio_form').children().filter('input[name|=lastfm_track]');
                    radio_track.attr('value',jsonData['lastfm_track_id'])
                    // set add to playlist form
                    $('#playlist_form').css('display','block');
                    playlist_track_song = $('#playlist_form').children().filter('input[name|=lastfm_track_song]');
                    playlist_track_song.attr('value',jsonData['lastfm_track_song_id']); 

                    setTimeout("Playlist.saveSongAsPlayed(" + escape(songId) + ","+escape(jsonData['lastfm_track_song_id'])+")", 20000);
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

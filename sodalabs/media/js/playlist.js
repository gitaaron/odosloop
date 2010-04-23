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
    currentSongOpened : false,
    lastSongLogged : false,
    player : false,

    loadSearch : function(q) {
        $('#search_container').html('<h3>loading...</h3>');
        $.get('/lastfm/search', {'q':unescape(q)}, function(data) 
        {
            $('#search_container').html(data);
        });
    }, 

    loadFeed : function() {
        $('#feed_container').html('<h3>loading...</h3>');
        $.get('/home/feed', function(data) {
            $('#feed_container').html(data);
        });
    },

    loadRadio: function(r) {
        $('#radio_container').html('<h3>loading...</h3>');
        $.get('/radio/ajax_get_similar', {'lastfm_track':r}, function(data) {
                $('#radio_container').html(data);
            });
    },

    saveSongAsPlayed : function(songId,lastFMTrackSongId) {
        if(songId == Playlist.currentSong && songId != Playlist.lastSongLogged) {
            $.post('/accounts/song_played/' + lastFMTrackSongId+'/', function(data) {
                    jsonData = JSON.parse(data);
                    if(jsonData['status']=='ok') {
                        Playlist.lastSongLogged = songId;
                    } else { 
                        console.log('song_played result failed because : ' + jsonData['message']);
                    }
            });
        } 
    },

    open : function(playlist_id, songId) {
        songId = parseInt(songId);
        song = Playlist.songs[playlist_id][songId];

        Playlist.currentSong = songId;
         
        $.get('/jukebox/get_closest_video/', song, function(data) {
                jsonData = JSON.parse(data);
                if(jsonData['status']=='ok') {
                    Playlist.currentSongOpened = jsonData;
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

    radio : function(playlist_id, songId) {
        songId = parseInt(songId);
        song = Playlist.songs[playlist_id][songId];
        Playlist.currentSong = songId;
        $.get('/jukebox/get_lastfm_track', song, function(data) {
            jsonData = JSON.parse(data);
            if(jsonData['status'] =='ok') {
                Radio.open(jsonData['lastfm_track_id']);
            } else {
                Playlist.markSongAsErred(songId);
            }
        });
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
        $('.now_playing').removeClass('now_playing');
        elem = Playlist.getElemById(songId);
        elem.addClass('now_playing');

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
        name = DocString.get()['menu'];
        return $('#'+name+'_item_'+id);
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
        Playlist.open(DocString.get()['menu'], songId);
    }

}

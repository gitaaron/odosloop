API_KEY = 'AI39si4G2-0d2C5E98vAfsM8RT5Z7h8md7wClPvY_Jhfu8oyonkYkjCuA_DBJehHGtPzb6UdIspQhf7M3Cc6_NW2pTT3t4uZ4A';

function onYouTubePlayerReady(playerId) {
    ytplayer = document.getElementById('ytPlayer');
    ytplayer.addEventListener('onStateChange','Playlist.onPlayerStateChange');
    ytplayer.addEventListener('onError','Playlist.onPlayerError');
    if(Playlist.shouldAutoPlay) {
        ytplayer.playVideo();
    }
}

var Playlist = {
    songs : new Array(),
    currentSong : false,
    currentListId : false,
    currentSongOpened : false,
    lastSongLogged : false,
    initialized : false,
    shouldPlayImmediately : false,

    init_once : function() {
        if (!Playlist.initialized) {
            Playlist.initialized = true;

            song = DocString.get()['song'];

            if (song) {
                Playlist.playIfSongInPlaylist(song);
            } 

        }
    },

    playIfSongInPlaylist : function(lastfmTrackId) {
        $.get('/lastfm/get/'+lastfmTrackId, function(data) {
            playlist_id = DocString.get()['menu'];
            if(!playlist_id) {
                playlist_id = 'feed';
            }

            $.each(Playlist.songs[playlist_id], function(i, song) {
                if(song['name']==data['name'] && song['artist']==data['artist']) {
                    Playlist.open(playlist_id, i);
                }
            });
        });
    },


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

    loadUserPlaylist : function(slug_name) {
        $('#userplaylist_container').html('<h3>loading...</h3>');
        $.get('/playlist/get/'+slug_name, function(data) {
                $('#userplaylist_container').html(data);
        });
    },

    saveSongAsPlayed : function(songId,lastFMTrackSongId) {
        if(songId == Playlist.currentSong && songId != Playlist.lastSongLogged) {
            $.post('/accounts/song_played/' + lastFMTrackSongId+'/', function(data) {
                    if(data['status']=='ok') {
                        Playlist.lastSongLogged = songId;
                    } else { 
                        console.log('song_played result failed because : ' + data['message']);
                    }
            });
        } 
    },

    open : function(playlist_id, songId) {

        songId = parseInt(songId);
        song = Playlist.songs[playlist_id][songId];

        Playlist.currentSong = songId;
        Playlist.currentListId = playlist_id; 
        // show loading div and hide video container
        $('#youtube_container').css('display','none');
        $('#youtube_container').html('<h3 id="title"></h3><div id="videoDiv"><iframe width="320" height="180" class="youtube-player" type="text/html" width="640" height="385"  frameborder="0></iframe></div>');
        $('#loadingVideoDiv').css('display','block');
        $.get('/jukebox/get_closest_video/', song, function(data) {
                if(data['status']=='ok') {
                    DocString.add({'song':data['lastfm_track_id']});
                    var t =  'odosloop - ' + song['artist'] + ' - ' + song['name'];
                    try {
                        $('#browser_title').html(t);
                    } catch(err) { 
                        document.title = t; 
                    }

                    Playlist.currentSongOpened = data;

                    Playlist.play(data['video_id'], data['video_title']);

                    setTimeout("Playlist.saveSongAsPlayed(" + escape(songId) + ","+escape(data['lastfm_track_song_id'])+")", 20000);


                } else { 
                    Playlist.markSongAsErred(playlist_id, songId);
                    Playlist.goToNext();
                }
        });
        return false;
    },

    getPlaylistSong : function(playlist_id, song_id) {
        songId = parseInt(song_id);
        song = Playlist.songs[playlist_id][song_id];
        return song;
    },

    getSongIdForSong : function(playlist_id, song) {
        id = $.inArray(song, Playlist.songs[playlist_id]);
    },

    markSongAsErred : function(playlist_id, song_id) {
        elem = Playlist.getElemById(playlist_id, song_id);
        elem.html('(error) ' + elem.html());
    },

    getElemById : function(playlist_id, song_id) { 
        return $('#'+playlist_id+'_item_'+song_id);
    }, 

    play : function(id,title) {
        /*
        * Simple player embed
        */
        songId = Playlist.currentSong;
        $('.now_playing').removeClass('now_playing');
        elem = Playlist.getListItem(Playlist.currentListId, songId);
        elem.addClass('now_playing');

        $('#title').html(title);

        // hide loading div and show video container
        $('#youtube_container').css('display','block');
        $('#loadingVideoDiv').css('display','none');

        /*
        // The video to load.
        var videoID = id;
        // Lets Flash from another domain call JavaScript
        var params = { allowScriptAccess: "always" , height:180, width:320 };
        // The element id of the Flash embed
        var atts = { id: "ytPlayer" };
        // All of the magic handled by SWFObject (http://code.google.com/p/swfobject/)
        swfobject.embedSWF("http://www.youtube.com/v/" + videoID + "&enablejsapi=1&playerapiid="+API_KEY,
                           "videoDiv", "320", "180", "8", null, null, params, atts);
        */
        var src = 'http://www.youtube.com/embed/' + id;
        $('.youtube-player').attr('src',src);
    },

    getListItem : function(playListId, songId) {
        name = DocString.get()['menu'];
        return $('#'+playListId+'_item_'+songId);
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
        Playlist.shouldAutoPlay = true;
        songId = Playlist.currentSong+1;
        Playlist.open(Playlist.currentListId, songId);
    },

    push : function(playlist_id, artist, name) {

        if (!Playlist.songs[playlist_id].length) {
            Playlist.songs[playlist_id] = new Array();
        }

        var obj = {'artist':artist, 'name':name};
        arr = Playlist.songs[playlist_id];
        arr.push(obj);

        l = arr.length;
        return l;
    }


}

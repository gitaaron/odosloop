var Radio = {
    init : function() {
        $(document).bind('hrefChanged', function(e, diff) {
            if(diff.menu=='radio' || diff.r) {
                if(diff.r) {
                    Playlist.loadRadio(diff.r);
                } else if (Playlist.currentSong || parseInt(Playlist.currentSong)==0) {
                    if (Playlist.currentSong==0) {
                        console.log('equals zero');
                    } else {
                        console.log('does not equal zero');
                    }
                    Radio.search(Playlist.getPlaylistSong(Playlist.currentListId, Playlist.currentSong));
                }
            }
        });

    },


    open : function(id) {
        DocString.add({'r':id});
        DocString.add({'menu':'radio'});
    },


    search : function(playlist_song) {
         $.get('/jukebox/get_lastfm_track/', playlist_song, function(data) {
            if(data['status'] =='ok') {
                Radio.open(data['lastfm_track_id']);
            } else {
                Playlist.markSongAsErred(playlist_song);
            }
        });       
    }

}

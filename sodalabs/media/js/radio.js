var Radio = {
    init : function() {
        $(document).bind('hrefChanged', function(e, diff) {
            if(diff.r) {
                Playlist.loadRadio(diff.r);
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
                Playlist.getSongIdForSong('radio',playlist_song);
                Playlist.markSongAsErred(playlist_song);
            }
        });       
    }

}

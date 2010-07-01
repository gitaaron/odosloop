var UserPlaylist = {

    init  : function() {
        $(document).bind('hrefChanged', function(e, diff) {
            if (diff.menu) {
                parts = diff.menu.split('_');
                if (parts[0]=='playlist') {
                    slug_name = parts[1];
                    Playlist.loadUserPlaylist(slug_name);
                }
            }
        });

    },
    create : function() {
        $.post('/playlist/create/', function() {
                $.get('/playlist/menu/'+DocString.get()['user'], function(data) {
                    $('#menu_container').html(data);
                });
        });
    },

    select : function(playlist_song_id, song_name, playlist_controller, userplaylist_name, userplaylist_id) { 
        playlist_id = $(playlist_controller).attr('id').split('_')[2];
        pl_song = Playlist.getPlaylistSong(playlist_id, playlist_song_id);
        UserPlaylist.addPlaylistSong(pl_song, song_name, userplaylist_name, userplaylist_id); 
    },



    addPlaylistSong : function(playlist_song, song_name, playlist_name, playlist_id) {
        $.get('/jukebox/get_lastfm_track/', playlist_song, function(data) {
                if(data['status'] =='ok') {
                    UserPlaylist.add(data['lastfm_track_id'], song_name, playlist_name, playlist_id);
                } 
        });
    },

    add : function(lastfm_track_id, song_name, playlist_name, playlist_id) {
        data = {'lastfm_track':lastfm_track_id};
        if(playlist_id) {
            data['playlist'] = playlist_id;
        }

        $.post('/playlist/add/', data, function(data) {
            if(data['status']=='ok') {
                alert(song_name + ' was added to ' + playlist_name + ' succesfully.');
            } else {
                alert('There was a problem adding ' + song_name + ' to ' + playlist_name);
            }

        });
    },
    

    editPlaylistItem : function(playlist_id) {
        editable_playlist = $('#editable_playlist_item_'+playlist_id);
        playlist_item = $('#playlist_item_'+playlist_id);
        editable_playlist.css({'display':'block'});
        playlist_item.css({'display':'none'});
    }, 

    finishedEditing : function(playlist_id) {
        user = DocString.get()['user'];
        if (!user) {
            user = '';
        }
        $.get('/playlist/menu/'+user, function(data) {
            $('#menu_container').html(data);
        });
    },

    savePlaylistItem : function(playlist_id) {
        name = $('#editable_playlist_name_'+playlist_id).attr('value');
        $.post('/playlist/save/', {'playlist_id':playlist_id, 'name':name}, function(data) {
            if (data['status']=='ok') {
                UserPlaylist.finishedEditing(playlist_id);
            } else {
                alert('There was a problem saving the playlist name');
            }
        });
    }


}

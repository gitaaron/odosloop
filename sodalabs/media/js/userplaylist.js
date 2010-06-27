var UserPlaylist = {
    create : function() {
        $.post('/playlist/create/', function() {
                $.get('/playlist/menu/'+DocString.get()['user'], function(data) {
                    $('#menu_container').html(data);
                });
        });
    },

    editPlaylistItem : function(playlist_id) {
        editable_playlist = $('#editable_playlist_item_'+playlist_id);
        playlist_item = $('#playlist_item_'+playlist_id);
        editable_playlist.css({'display':'block'});
        playlist_item.css({'display':'none'});
    }, 

    finishedEditing : function(playlist_id) {
        $.get('/playlist/menu/'+diff.user, function(data) {
            $('#menu_container').html(data);
        });
    },

    savePlaylistItem : function(playlist_id) {
        name = $('#editable_playlist_name_'+playlist_id).attr('value');
        $.post('/playlist/save/', {'playlist_id':playlist_id, 'name':name}, function(data) {
            if (data['status']=='ok') {
                Menu.finishedEditing(playlist_id);
            } else {
                alert('There was a problem saving the playlist name');
            }
        });
    }


}

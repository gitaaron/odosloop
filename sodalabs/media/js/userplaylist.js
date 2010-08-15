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

        e_m = User.eventManager;
        $(e_m).bind('user_login', UserPlaylist.update);

    },

    update : function() {
        $.get('/playlist/json_list/', function(data) {
            if (data['status']=='ok') {
                playlists = data['playlists'];
                html = '\
    <li class="vertical_item">\
        <a class="action" onclick="return UserPlaylist.select(\'<#= playlist_song_id #>\', \'<#= playlist_id #>\', \'<#= userplaylist_name #>\', \'<#= userplaylist_id #>\');">\
            <div><#= userplaylist_name #></div>\
        </a>\
    </li>';
                $('.userplaylist_container').each(function() {
                    elem = this;
                    id = $(elem).attr('id');
                    comps = id.split('_')
                    playlist_id = comps[comps.length-2];
                    playlist_song_id = comps[comps.length-1]; 
                    list_elems_html = '';
                    $.each(playlists, function(k,userplaylist) {
                        list_elems_html += template.parse(html, {playlist_song_id:playlist_song_id, playlist_id:playlist_id, userplaylist_name:userplaylist['name'], userplaylist_id:userplaylist['id']});
                    });
                    $(elem).html(list_elems_html);
                }); 

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

    select : function(playlist_song_id, playlist_id, userplaylist_name, userplaylist_id) { 
        pl_song = Playlist.getPlaylistSong(playlist_id, playlist_song_id);
        song_name = pl_song['name'];
        UserPlaylist.addPlaylistSong(pl_song, song_name, userplaylist_name, userplaylist_id); 
    },

    selectDummy : function(playlist_song_id, song_name, playlist_id, userplaylist_name) {
        pl_song = Playlist.getPlaylistSong(playlist_id, playlist_song_id);
        UserPlaylist.addPlaylistSong(pl_song, song_name, userplaylist_name, null);
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

        if(!playlist_name) {
            playlist_name = 'unknown';
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

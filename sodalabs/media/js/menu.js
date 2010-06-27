var Menu = {
    itemResults : {},
    init : function() {
        $(document).bind('hrefChanged', function(e,diff) {
            if(diff.menu) {
                Menu.setMenuItem(diff.menu,diff);
            }
            if(diff.user) {
                $.get('/playlist/menu/'+diff.user, function(data) {
                    $('#menu_container').html(data);
                });
            }
        });

        $('#menu_list a').bind('click',function() {
            if (!DocString.get()['r'] && Playlist.currentSong) {
                Radio.search(Playlist.getPlaylistSong(Playlist.currentListId, Playlist.currentSong));
            } else { 
                DocString.add({'menu':$(this).attr('id')}); 
            }
            //$(document).trigger('menuChanged',{'menu_item':$(this).attr('id')});
        });

    }, 
    setMenuItem : function(name,params) {
        Menu.highlightMenuItem(name);
        $('.playlist_container').each(function() {
            $(this).css('display','none');
        });
        $('#'+name+'_container').css('display','block');
    },

    highlightMenuItem : function(name) {
        $('.selected').each(function() {
            $(this).removeClass('selected');
        });
        $('#'+name).addClass('selected');
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
        console.log('name : ' + name);
        $.post('/playlist/save/', {'playlist_id':playlist_id, 'name':name}, function(data) {
            if (data['status']=='ok') {
                Menu.finishedEditing(playlist_id);
            } else {
                alert('There was a problem saving the playlist name');
            }
        });
    }
}

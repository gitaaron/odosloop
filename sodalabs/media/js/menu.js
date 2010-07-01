var Menu = {
    itemResults : {},
    menuItem : false,
    init : function() {
        Menu.menuItem = false;
        $(document).bind('hrefChanged', function(e,diff) {
            if(diff.menu) {
                Menu.setMenuItem(diff.menu);
            }
            if(diff.user) {
                $.get('/playlist/menu/'+diff.user, function(data) {
                    $('#menu_container').html(data);
                });
            }
        });

        if (DocString.get()['menu']) { 
            Menu.setMenuItem(DocString.get()['menu']);
        } else {
            Menu.setMenuItem('feed');
        }

        $('#menu_list a').bind('click', function() {
            DocString.add({'menu':$(this).attr('id')});
        });

        /*(
        $('#menu_list a').bind('click',function() {
            if (!DocString.get()['r'] && Playlist.currentSong) {
                Radio.search(Playlist.getPlaylistSong(Playlist.currentListId, Playlist.currentSong));
            } else { 
                DocString.add({'menu':$(this).attr('id')}); 
            }
            //$(document).trigger('menuChanged',{'menu_item':$(this).attr('id')});
        });
        */

    }, 
    setMenuItem : function(name) {
        parts = name.split('_');
        if (parts[0] == 'playlist') {
            name='userplaylist';
        }
        if (name!= Menu.menuItem) {
            Menu.menuItem = name;
            Menu.highlightMenuItem(name);
            $('.playlist_container').each(function() {
                $(this).css('display','none');
            });
            $('#'+name+'_container').css('display','block');
        }
    },

    highlightMenuItem : function(name) {
        $('.selected').each(function() {
            $(this).removeClass('selected');
        });
        $('#'+name).addClass('selected');
    } 

}

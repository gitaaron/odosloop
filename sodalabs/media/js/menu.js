var Menu = {
    itemResults : {},
    init : function() {
        $(document).bind('hrefChanged', function(e,diff) {
            if(diff.menu) {
                Menu.setMenuItem(diff.menu,diff);
            }
        });

        $('#menu_list a').bind('click',function() {
            DocString.add({'menu':$(this).attr('id')}); 
            $(document).trigger('menuChanged',{'menu_item':$(this).attr('id')});
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
    }

}

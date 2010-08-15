var Feed = {

    loaded : false,

    init : function() {
     $(document).bind('hrefChanged', function(e, diff) {
            if(diff.menu=='feed' && ! Feed.loaded) { 
                Playlist.loadFeed();    
                Feed.loaded = true;
            } else if(diff.isFirst && ! diff.menu) {
                Playlist.loadFeed(); 
                Feed.loaded = true;
            }

        });


    }



}

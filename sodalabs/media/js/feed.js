var Feed = {
    init : function() {
     $(document).bind('hrefChanged', function(e, diff) {
            if(diff.menu=='feed' && !$('feed_container').html()) { 
                Playlist.loadFeed();    
            } else if(diff.isFirst) {
                Playlist.loadFeed(); 
            }
        });


    }



}

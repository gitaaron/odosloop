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

}

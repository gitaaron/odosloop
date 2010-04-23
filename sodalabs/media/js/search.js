var Search = {
    init : function() {
        $('#music_search_form').submit(function() {
            form = $('#music_search_form')
            q = form.children().filter('input[name|=q]');
            DocString.add({'q':q.val(),'menu':'search'})
            return false;
        });

        $(document).bind('hrefChanged', function(e, diff) {
                if(diff.q) {
                    Playlist.loadSearch(diff.q);
                }
        });


    }

}

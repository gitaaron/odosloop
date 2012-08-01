var g_playlist_item_tpl;
define(['jade!../tpl/playlist_item'], function(playlist_item_tpl) {
    g_playlist_item_tpl = playlist_item_tpl;
    return {
        playlist_item_tpl:playlist_item_tpl
    }

});

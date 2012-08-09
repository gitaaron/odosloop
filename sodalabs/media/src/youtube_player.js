/* Interacting with flash video player */

function onPlayerStateChange(state) {
    if(state==0) {
       vent.trigger('goToNext'); 
    } 
}

function onPlayerStateError(code) {

}

function onYouTubePlayerReady(playerId) {
    console.log('onYouTubePlayer');
    ytplayer = document.getElementById('ytPlayer');
    ytplayer.addEventListener('onStateChange','onPlayerStateChange');
    ytplayer.addEventListener('onError','onPlayerError');
    ytplayer.playVideo();
}

define(['exports'], function(exports) {

    exports.play = function(video_id, video_title) {
            console.log('play : ' + video_id);
            $('#title').html(video_title);
            $('.now_playing').removeClass('now_playing');
            $(this.el).addClass('now_playing');
            // hide loading div and show video container
            $('#youtube_container').show();
            $('#loadingVideoDiv').hide();


            // Lets Flash from another domain call JavaScript
            var params = { allowScriptAccess: "always" , height:200, width:350, wmode:'opaque'};
            // The element id of the Flash embed
            var atts = { id: "ytPlayer" , 'wmode':'opaque'};
            // All of the magic handled by SWFObject (http://code.google.com/p/swfobject/)
            swfobject.embedSWF("http://www.youtube.com/v/" + video_id + "&version=3&enablejsapi=1&playerapiid="+API_KEY,
                               "videoDiv", "350", "200", "8", null, null, params, atts);


        }



});

# Create your views here.
import urllib
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse,Http404
import gdata.youtube
import gdata.youtube.service
import django.utils.simplejson as json
from sodalabs.lastfm.models import Track
from sodalabs.jukebox.models import LastFMTrackSong,Song
from sodalabs.accounts.models import PlayHistory

YOUTUBE_API_KEY = 'AI39si4G2-0d2C5E98vAfsM8RT5Z7h8md7wClPvY_Jhfu8oyonkYkjCuA_DBJehHGtPzb6UdIspQhf7M3Cc6_NW2pTT3t4uZ4A'

def open(request):
    client = gdata.youtube.service.YouTubeService()
    client.developer_key = YOUTUBE_API_KEY
    query = gdata.youtube.service.YouTubeVideoQuery()
    name = request.GET.get('name',False)
    artist = request.GET.get('artist',False)
    q = request.GET.get('q','')
    if not name:
        return HttpResponse(json.dumps({'status':'failed','message':'name missing'}),content_type="application/json")

    if artist:
        # see if lastfm track already exists
        try:
            track = Track.objects.get(name=name,artist=artist)
        except Track.DoesNotExist:
            track = Track(name=name,artist=artist,search=q)
            track.save()

        search = artist + ' - ' + name


    query.vq = _unescape(urllib.unquote(search))
    query.max_results = 25
    try:
        feed = client.YouTubeQuery(query)
    except KeyError:
        return HttpResponse(json.dumps({'status':'failed','message':'a problem occured while searching youtube for the appropriate song'}),content_type="application/json")
    video_id = ''
    embedable_found = False
    for entry in feed.entry:
        if not entry.noembed:
            embedable_found = True
            break

    if not feed.entry:
        return HttpResponse(json.dumps({'status':'failed', 'message':'no results returned'}),content_type="application/json")
    elif not embedable_found:
        return HttpResponse(json.dumps({'status':'failed', 'message':'no embedable songs found'}),content_type="application/json")
    else:
        # see if this song already exists
        video_id = entry.id.text.split('/').pop()
        video_title = entry.title.text 
        try:
            song = Song.objects.get(media_id=video_id)
        except Song.DoesNotExist:
            song = Song(media_id=video_id,media_title=video_title)
            song.save()

        try:
            lastfm_track_song = LastFMTrackSong.objects.get(lastfm_track=track,song=song)
        except LastFMTrackSong.DoesNotExist:
            lastfm_track_song = LastFMTrackSong(lastfm_track=track,song=song)
            lastfm_track_song.save()

        if request.user.is_authenticated():
            song_played = PlayHistory(musiphile=request.user,song=lastfm_track_song) 
            song_played.save()

        dict = {'status':'ok', 'video_id':entry.id.text.split('/').pop(), 'video_title':entry.title.text,'song_id':song.id,'lastfm_track_id':track.id}

    return HttpResponse(json.dumps(dict), content_type="application/json")




##PRAGNOTE Taken from http://effbot.org/zone/re-sub.htm#unescape-html

import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def _unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

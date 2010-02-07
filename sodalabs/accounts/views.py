# Create your views here.
import datetime
import simplejson as json
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site, RequestSite
from django.template import RequestContext

from sodalabs import settings
from sodalabs.accounts.forms import AuthenticationForm,UserCreationForm
from sodalabs.rest_ws.helpers import ResponseBadRequest
from sodalabs.accounts.models import Musiphile,PlayHistory
from sodalabs.jukebox.models import LastFMTrackSong



@login_required
def profile(request, username=None):
    """
    For now just look the user up in last.fm and display their info.
    """
    musiphile = Musiphile.objects.get(id=request.user.id)
    songs_played = PlayHistory.objects.filter(musiphile=musiphile).order_by('created_at').reverse()[0:50]

    tracks = []
    for play in songs_played:
        lastfm_track = play.song.lastfm_track
        tracks.append({'name':lastfm_track.name,'artist':lastfm_track.artist})
    return direct_to_template(request, 'accounts/profile.html', {'playlist_title':'scrobbled on odosloop', 'lastfm_tracks': tracks, 'username':username})

def anonymous(request):
    songs_played = request.session.get('playhistory',[])
    tracks = []
    for song in songs_played:
        tracks.append({'name':song['name'],'artist':song['artist']})

    return direct_to_template(request, 'accounts/profile.html', {'playlist_title':'scrobbled on odosloop','lastfm_tracks':tracks})

def flush(request):
    request.session.flush()
    return HttpResponse('ok')

def song_played(request,lastfm_track_song_id):
    try:
        lastfm_track_song = LastFMTrackSong.objects.get(id=lastfm_track_song_id)
    except LastFMTrackSong.DoesNotExist:
        return HttpResponse(json.dumps({'status':'failed','message':'Could not find song for specified id : ' + lastfm_track_song_id}),content_type="application/json")


    if request.user.is_authenticated():
        song_played = PlayHistory(musiphile=request.user,song=lastfm_track_song)
        song_played.save()
    else:
        lastfm_track = lastfm_track_song.lastfm_track
        playhistory = request.session.get('playhistory',[])
        playhistory.append({'lastfm_track_song_id':lastfm_track_song_id,'artist':lastfm_track.artist,'name':lastfm_track.name, 'date':datetime.datetime.now()})
        request.session['playhistory'] = playhistory
    return HttpResponse(json.dumps({'status':'ok'}),content_type="application/json")


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def signup(request, template_name='accounts/signup.html',redirect_field_name='next'):
    '''
    Override built-in django login to add following featured:
        - also pass register form
        - use email address to authenticate
        - if session contains a lightbox, save to user list
    '''
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    # Light security check -- make sure redirect_to isn't garbage
    if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    if request.method == "POST":
        action = request.POST.get('action', False)
        if action=='login':
            login_form = AuthenticationForm(data=request.POST)
            register_form = UserCreationForm()
            if login_form.is_valid():
                from django.contrib.auth import login
                user = login_form.get_user()
                login(request, user)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                # @TODO save playlists here 

                return HttpResponseRedirect(redirect_to)
        elif action=='register':
            login_form = AuthenticationForm(request)
            # create new dict for copying email into username because request.POST is immutable
            musiphile_email = request.POST.get('musiphile_email','')
            password1 = request.POST.get('password1','')
            password2 = request.POST.get('password2','')
            data = {
                    'username' : musiphile_email,
                    'musiphile_email' : musiphile_email,
                    'password1' : password1,
                    'password2' : password2,
            }


            register_form = UserCreationForm(data)
            if register_form.is_valid():
                user = register_form.save()

                # log user in
                user = authenticate(musiphile_email=user.musiphile_email, password=request.POST['password1'])
                from django.contrib.auth import login
                login(request,user)
                return HttpResponseRedirect(redirect_to)
        else:
            return ResponseBadRequest()

    else: # request is get, render page
        login_form = AuthenticationForm(request)
        register_form = UserCreationForm()

    request.session.set_test_cookie()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)



    return render_to_response(template_name, {
        'login_form': login_form,
        'register_form': register_form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
    return HttpResponse('ok')
signup = never_cache(signup)



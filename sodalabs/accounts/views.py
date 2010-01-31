# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site, RequestSite
from django.template import RequestContext

from sodalabs import settings
from sodalabs.accounts.forms import AuthenticationForm,UserCreationForm
from sodalabs.rest_ws.helpers import ResponseBadRequest

from sodalabs.lastfm import make_lastfm_request,get_tracks,error_path,user_path


def profile(request, username=None):
    """
    For now just look the user up in last.fm and display their info.
    """
    #@TODO error templates do not exist anymore
    if not username:
        username = request.GET.get('username',None)
    if not username:
        return direct_to_template(request,'playlist/index.html',{'message':'Your request is missing a required paramater.'})
    # compile lastfm list of name,artist 

    doc = make_lastfm_request('user.getrecenttracks',{'limit':'100','user':username})
    if not doc:
        return direct_to_template(request, 'playlist/index.html',{'message':'A problem occured accessing the last.fm api.'})
    errors = error_path(doc)
    if errors:
        return direct_to_template(request, 'playlist/index.html',{'message':errors[0].text_content()})

    lastfm_recents = []
    lastfm_recents = get_tracks(doc) 

    lastfm_friends = []
    doc = make_lastfm_request('user.getfriends',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_friends.append({'name':user.find('name').text_content()})

    lastfm_neighbours = []
    doc = make_lastfm_request('user.getneighbours',{'user':username})
    users = user_path(doc)
    for user in users:
        lastfm_neighbours.append({'name':user.find('name').text_content()})

    return direct_to_template(request, 'accounts/profile.html', {'lastfm_recents': lastfm_recents, 'lastfm_friends':lastfm_friends, 'lastfm_neighbours':lastfm_neighbours, 'username':username})





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



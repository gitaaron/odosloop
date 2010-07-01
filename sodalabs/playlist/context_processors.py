from sodalabs.accounts.models import Musiphile

from sodalabs.playlist.models import Playlist

def saved_playlist(request):
    user_playlists = None
    if request.user.is_authenticated():
        musiphile = Musiphile.objects.from_request(request)
        if musiphile:
            user_playlists = Playlist.objects.filter(users=musiphile)

    return {'saved_playlists':user_playlists}

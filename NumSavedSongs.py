def NumSavedSongs():
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_saved_tracks(limit = 1, offset = 0, market = None)
    num_songs = song['total']
    return num_songs
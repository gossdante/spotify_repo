import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import math
import time

def NumSavedSongs():
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_saved_tracks(limit = 1, offset = 0, market = None)
    num_songs = song['total']
    return num_songs

# Make a function that will make a plus delta for tempos
def LowHigh(target_tempo, range):
    each_side = range/2
    lowtempo = target_tempo - each_side
    hightempo = target_tempo + each_side
    return lowtempo,hightempo

# Function to select songs within a range of tempos
def TempoRange(data,target_tempo,range):
    each_side = range/2
    lowtempo = target_tempo - each_side
    hightempo = target_tempo + each_side
    SongsInRange = data[(data['tempo'] > lowtempo) & (data['tempo'] < hightempo)]
    TrackIDRange = SongsInRange['Track_ID']
    return SongsInRange, TrackIDRange

# Make a function to create a playlist & add songs given track id's
def PlaylistMaker(Tracks,name_input):
    import math
    # Get user_id
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    profile = sp.current_user()
    user_id = profile['id']
    # Get playlist_name
    playlist_name = name_input
    # Public or not
    Public = False
    # Collaborative or not
    Collab = False
    #Collab = input("Would you like this playlist ot be collaborative or not? Note the response must be True or False: ")
    # Tracks needs to be an input vector

    # Create playlist
    p = sp.user_playlist_create(user_id, playlist_name, public=Public, collaborative = Collab)
    # Get playlist id
    playlist_id = p['id']

    # loop to add songs - note that only 100 songs can be added at a time
    if len(Tracks) < 100:
        sp.user_playlist_add_tracks(user_id,playlist_id,tracks = Tracks, position = None)
        print("Playlist Made")
    elif len(Tracks) > 100:
        # First get how many times 100 goes into the length, and round up to decide the number of loops
        timesin = math.ceil(len(Tracks)/100)
        # the loop will always start with the first 100 if the loop has more than 100, or the total number of tracks if less than
        firstval = 0
        secondval = 100
        i = 0
        while i <= timesin:
            if secondval < len(Tracks):
                sp.user_playlist_add_tracks(user_id, playlist_id, tracks = Tracks[firstval:secondval],position = None)
                firstval = secondval
                secondval = secondval + 100 # move to the next 100
                i = i + 1 # next loop iteration
            else: 
                secondval = len(Tracks) # if you have less than 100 in a group of tracks
                sp.user_playlist_add_tracks(user_id, playlist_id, tracks = Tracks[firstval:secondval], position = None)
                print("Playlist Made")
                
    # Make a function to get all saved songs 
def SavedSongs():
    import pandas as pd
    import math
    import time
    # Now we need to make a loop that will go through all saved songs
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    # Step 1: How many saved songs do we have?
    # You can get this by doing a current_user_saved_tracks search
    song = sp.current_user_saved_tracks(limit = 1, offset = 0, market = None)
    num_songs = song['total']
    # print('You have ',num_songs,'saved songs')

    # Initialize Variables
    track_name = [] 
    track_id = []
    artist_name = []
    artist_id = []
    artist_num = []
    track_len = []
    trackfeatures = pd.DataFrame(columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
           'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
           'time_signature'])
    # The limit for current_user_saved_tracks is 20, so we need to round up to the nearest multiple of 20
    # in the math package the ceil function will round up
    num_loops = math.ceil(num_songs/20)
    
    # Now make a big loop that will go through it all
    for i in range(0,num_loops+1):
        print((num_loops+1-i),'Loops Left')
        result = sp.current_user_saved_tracks(limit = 20, offset = (i*20), market = None)
        # sleep
        time.sleep(5)# 5 second sleep
        # Loop through saved tracks
        for item in result['items']:
            track = item['track']
            track_name.append(track['name'])
            track_id.append(track['id']) 
            try: 
                audio = (sp.audio_features(tracks = track['id']))
                audio = pd.DataFrame(audio)
                audio = audio.reset_index(inplace=False)
            except:
                pass
            trackfeatures = pd.concat([trackfeatures,audio],axis=0,ignore_index=True)
         
            artist_name.append(track['artists'][0]['name'])
            artist_id.append(track['artists'][0]['id'])
            artist_num.append(len(track['artists']))
            track_len.append(track['duration_ms']/1000)
    # Convert to DF
    Track_Name=pd.DataFrame(track_name,columns=['Track_Name'])
    Track_ID=pd.DataFrame(track_id,columns=['Track_ID'])
    Artist_Name=pd.DataFrame(artist_name,columns=['Artist_Name'])
    Artist_ID=pd.DataFrame(artist_id,columns=['Artist_ID'])
    Artist_Num=pd.DataFrame(artist_num,columns=['Artist_Num'])
    Track_Len=pd.DataFrame(track_len,columns=['Track_Len'])
    # Combine
    df = pd.concat([Track_Name,Track_ID,Artist_Name,Artist_ID,Artist_Num,Track_Len],axis =1)

    # Now Merge with df
    trackfeatures =trackfeatures.rename(columns={'id':'Track_ID'})
    data = pd.merge(df,trackfeatures,on=['Track_ID'])
    return data


# Make the app
st.title('Spotify Tool')
st.write('---')


st.header("Text Input to Access Spotify API")
client_ID = st.text_input("Please Input your Client ID then press enter", "")
if st.button("Check Client ID"):
    st.write(client_ID)
client_secret = st.text_input("Please Input your Client Secret then press enter", "")
if st.button("Check Client Secret"):
    st.write(client_secret)
redirect = st.text_input("Please Input your redirect url then press enter", "")
if st.button("Check Redirect URL"):
    st.write(redirect)

os.environ["SPOTIPY_CLIENT_ID"] = client_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = redirect

st.write('---')
st.header('Get Saved Songs')
st.write('Press the button below to find out how many saved songs you have')

if st.button("How many saved songs do you have?"):
    a = NumSavedSongs()
    st.write('You Have:',a,'Saved Songs')

#st.write('Press the button below to load in all your saved songs')

#if st.button("Get saved songs"):
#    b = SavedSongs()
#    b['count'] = 1
#    c = b.groupby('Artist_Name')['count'].sum()[0]
#    #st.write(((num_loops+1-i),'Loops Left'))

#    st.write('Your favorite artist is: ',c)


#st.write('---')
#st.header("Make Playlist")
#tempo = st.text_input('What target tempo would you like? Remember to press enter.')
#tol = st.text_input('How much tolerance d you want? e.g. 2 bpm above and below is a tolerance of 4.')
#namep = st.text_input('What would you like to name your playlist?')

#if st.button("Create Playlist"):
#    songs,tracks = TempoRange(b,tempo,tol)
#    p = PlaylistMaker(tracks,namep)
#    st.write('Check your spotify')

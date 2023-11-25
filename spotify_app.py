import streamlit as st
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import math
import time
import spotipy.util as util


def NumSavedSongs():
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_saved_tracks(limit = 1, offset = 0, market = None)
    num_songs = song['total']
    return num_songs

def CurrentFavorites():
    # Initialize Variables
    track_name = [] 
    track_id = []
    artist_name = []
    artist_id = []
    artist_num = []
    track_len = []
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_top_tracks(limit = 20, offset = 0,time_range='short_term')

    for item in song['items']:
        track_name.append(item['name'])
        track_id.append(item['id'])   
        artist_name.append(item['artists'][0]['name'])
        artist_id.append(item['artists'][0]['id'])
        artist_num.append(len(item['artists']))
        track_len.append(item['duration_ms']/1000)
    # Convert to DF
    Track_Name=pd.DataFrame(track_name,columns=['Track_Name'])
    Track_ID=pd.DataFrame(track_id,columns=['Track_ID'])
    Artist_Name=pd.DataFrame(artist_name,columns=['Artist_Name'])
    Artist_ID=pd.DataFrame(artist_id,columns=['Artist_ID'])
    Artist_Num=pd.DataFrame(artist_num,columns=['Artist_Num'])
    Track_Len=pd.DataFrame(track_len,columns=['Track_Len'])
    # Combine
    df = pd.concat([Track_Name,Track_ID,Artist_Name,Artist_ID,Artist_Num,Track_Len],axis =1)
    return df

def CurrentFavorites_recommendations():
    # Initialize Variables
    track_name = [] 
    track_id = []
    artist_name = []
    artist_id = []
    artist_num = []
    track_len = []
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_top_tracks(limit = 20, offset = 0,time_range='short_term')

    for item in song['items']:
        track_name.append(item['name'])
        track_id.append(item['id'])   
        artist_name.append(item['artists'][0]['name'])
        artist_id.append(item['artists'][0]['id'])
        artist_num.append(len(item['artists']))
        track_len.append(item['duration_ms']/1000)
    # Convert to DF
    Track_Name=pd.DataFrame(track_name,columns=['Track_Name'])
    Track_ID=pd.DataFrame(track_id,columns=['Track_ID'])
    Artist_Name=pd.DataFrame(artist_name,columns=['Artist_Name'])
    Artist_ID=pd.DataFrame(artist_id,columns=['Artist_ID'])
    Artist_Num=pd.DataFrame(artist_num,columns=['Artist_Num'])
    Track_Len=pd.DataFrame(track_len,columns=['Track_Len'])
    # Combine
    df = pd.concat([Track_Name,Track_ID,Artist_Name,Artist_ID,Artist_Num,Track_Len],axis =1)
    track_list = df['Track_ID'].to_list()
    # Get Recommendations
    track_ids = []
    idx = 0
    while idx <19:
        idx2 = idx+5
        song = sp.recommendations(seed_tracks = track_list[idx:idx2],limit=25, time_range='short_range')
        for item in song['tracks']:
            track_ids.append(item['id'])
        idx = idx + 5
    return track_ids

def CurrentFavorites_recommendations_tempo(low,high):
    # Initialize Variables
    track_name = [] 
    track_id = []
    artist_name = []
    artist_id = []
    artist_num = []
    track_len = []
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_top_tracks(limit = 20, offset = 0,time_range='short_term')

    for item in song['items']:
        track_name.append(item['name'])
        track_id.append(item['id'])   
        artist_name.append(item['artists'][0]['name'])
        artist_id.append(item['artists'][0]['id'])
        artist_num.append(len(item['artists']))
        track_len.append(item['duration_ms']/1000)
    # Convert to DF
    Track_Name=pd.DataFrame(track_name,columns=['Track_Name'])
    Track_ID=pd.DataFrame(track_id,columns=['Track_ID'])
    Artist_Name=pd.DataFrame(artist_name,columns=['Artist_Name'])
    Artist_ID=pd.DataFrame(artist_id,columns=['Artist_ID'])
    Artist_Num=pd.DataFrame(artist_num,columns=['Artist_Num'])
    Track_Len=pd.DataFrame(track_len,columns=['Track_Len'])
    # Combine
    df = pd.concat([Track_Name,Track_ID,Artist_Name,Artist_ID,Artist_Num,Track_Len],axis =1)
    track_list = df['Track_ID'].to_list()
    # Get Recommendations
    track_ids = []
    idx = 0
    while idx <19:
        idx2 = idx+5
        song = sp.recommendations(seed_tracks = track_list[idx:idx2], limit=25, time_range='short_range',
                                  min_tempo = low,max_tempo = high)
        for item in song['tracks']:
            track_ids.append(item['id'])
        idx = idx + 5
    return track_ids

def CurrentFavorites_recommendations_custom(low,high,min_energy,max_energy,min_dance,max_dance):
    # Initialize Variables
    track_name = [] 
    track_id = []
    artist_name = []
    artist_id = []
    artist_num = []
    track_len = []
    # Set scope
    scope = "user-library-read playlist-read-private playlist-modify-public playlist-modify-private"
    # Authorize
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song = sp.current_user_top_tracks(limit = 20, offset = 0,time_range='short_term')

    for item in song['items']:
        track_name.append(item['name'])
        track_id.append(item['id'])   
        artist_name.append(item['artists'][0]['name'])
        artist_id.append(item['artists'][0]['id'])
        artist_num.append(len(item['artists']))
        track_len.append(item['duration_ms']/1000)
    # Convert to DF
    Track_Name=pd.DataFrame(track_name,columns=['Track_Name'])
    Track_ID=pd.DataFrame(track_id,columns=['Track_ID'])
    Artist_Name=pd.DataFrame(artist_name,columns=['Artist_Name'])
    Artist_ID=pd.DataFrame(artist_id,columns=['Artist_ID'])
    Artist_Num=pd.DataFrame(artist_num,columns=['Artist_Num'])
    Track_Len=pd.DataFrame(track_len,columns=['Track_Len'])
    # Combine
    df = pd.concat([Track_Name,Track_ID,Artist_Name,Artist_ID,Artist_Num,Track_Len],axis =1)
    track_list = df['Track_ID'].to_list()
    # Get Recommendations
    track_ids = []
    idx = 0
    while idx <19:
        idx2 = idx+5
        song = sp.recommendations(seed_tracks = track_list[idx:idx2], limit=25, time_range='short_range',
                                  min_tempo = low,max_tempo = high,
                                  min_energy = min_energy, max_energy = max_energy,
                                  min_danceability = min_dance, max_danceability = max_dance)
        for item in song['tracks']:
            track_ids.append(item['id'])
        idx = idx + 5
    return track_ids

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
    if len(Tracks) <= 100:
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
                
  

# Make the app
st.title('Spotify Tool')
st.write('This is a streamlit app that allows you to gather your favorite songs, make them into a playlist, find new songs that fit your current vibe, and customize making new playlists based on tempo, danceability, and energy that are recommended based on your current favorites.')
st.write('This app requires you have a spotify developer account which you can make at https://developer.spotify.com/ ')
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
st.header("Top Songs")

if st.button("How many saved songs do you have?"):
    a = NumSavedSongs()
    st.write('You Have:',a,'Saved Songs')

if st.button('Press the button to get your 20 top songs at the moment'):
    top_songs = CurrentFavorites()
    top_tracks = top_songs['Track_ID']
    st.write('Done!')
    st.write('Your top song atm is:',top_songs['Track_Name'][0])
    st.table(top_songs)
    
st.write('---')
st.header("Make Playlist of your current top songs")
playlist_name = st.text_input('What would you like to name the playlist?')
if st.button('Make the playlist'):
    top_songs = CurrentFavorites()
    top_tracks = top_songs['Track_ID']
    p = PlaylistMaker(top_tracks, playlist_name)
    st.write('Done!')
    st.table(top_songs)
    
st.write('---')
st.header("Make Playlist with recommendations from your top songs")
playlist_name2 = st.text_input('What would you like to name the playlist? ')
if st.button('Are you ready?'):
    tracks = CurrentFavorites_recommendations()
    p2 = PlaylistMaker(tracks, playlist_name2)
    st.write('Completed!')


st.write('---')
st.header("Make Playlist with recommendations from your top songs using a tempo target")
tempo = st.number_input('What target tempo would you like? Remember to press enter.')
tol = st.number_input('What is an allowable tolerance? (eg 5bpm)')
playlist_name3 = st.text_input('What would you like to name the playlist?  ')
if st.button('Did you fill both inputs? Great lets go!'):
    low,high = LowHigh(tempo,tol)
    tempo_tracks = CurrentFavorites_recommendations_tempo(low,high)
    p3 = PlaylistMaker(tempo_tracks, playlist_name3)
    st.write('Check Spotify!')


st.write('---')
st.header('(Mostly) Customizable playlist')
#tempo2 = st.selectbox(
#   "What target tempo would you like?",
#   ("100",'105','110','115','120','125','130','135','140','145','150','155','160','165','170','175','180','185'),
#   placeholder="None",
#)
#tol2 = st.selectbox(
#    'What tolerance would you like?',
#    ('1','2','3','4','5','6','7','8','9','10')
#)
#energy = st.slider('Select an energy',0.0,1.0,0.5,0.01)
#dance = st.slider('Select a danceability',0.0,1.0,0.5,0.01)
tempo2 = st.number_input('What target tempo would you like? Remember to press enter. ')
tol2 = st.number_input('What is an allowable tolerance? (eg 5bpm) ')
energyhighlow = st.selectbox(
    'Would you like high energy or low energy?',
    ('High Energy','Low Energy'),
    placeholder='Please select an energy',
)

dancehighlow = st.selectbox(
    'Would you like high or low danceability?',
    ('High Danceability','Low Danceability'),
    placeholder = 'Please select a danceability',
)

playlist_name4 = st.text_input('What would you like to name the playlist?   ')
if st.button('Generate'):
    low,high = LowHigh(tempo2,tol2)
    if (energyhighlow == 'High Energy') & (dancehighlow == 'High Danceability'):
        min_energy = 0.5
        max_energy = 1.0
        min_dance = 0.5
        max_dance = 1.0
        custom_tracks = CurrentFavorites_recommendations_custom(low,high,min_energy,max_energy,min_dance,max_dance)
        p4 = PlaylistMaker(custom_tracks, playlist_name4)
        st.write('Check Your Spotify!')
    elif (energyhighlow == 'High Energy') & (dancehighlow == 'Low Danceability'):
        min_energy = 0.5
        max_energy = 1.0
        min_dance = 0.0
        max_dance = 0.5
        custom_tracks = CurrentFavorites_recommendations_custom(low,high,min_energy,max_energy,min_dance,max_dance)
        p4 = PlaylistMaker(custom_tracks, playlist_name4)
        st.write('Check Your Spotify!')
    elif (energyhighlow == 'Low Energy') & (dancehighlow == 'High Danceability'):
        min_energy = 0.0
        max_energy = 0.5
        min_dance = 0.5
        max_dance = 1.0
        custom_tracks = CurrentFavorites_recommendations_custom(low,high,min_energy,max_energy,min_dance,max_dance)
        p4 = PlaylistMaker(custom_tracks, playlist_name4)
        st.write('Check Your Spotify!')
    elif (energyhighlow == 'Low Energy') & (dancehighlow == 'Low Energy'):
        min_energy = 0.0
        max_energy = 0.5
        min_dance = 0.0
        max_dance = 0.5
        custom_tracks = CurrentFavorites_recommendations_custom(low,high,min_energy,max_energy,min_dance,max_dance)
        p4 = PlaylistMaker(custom_tracks, playlist_name4)
        st.write('Check Your Spotify!')

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

EMOTIONAL_SONGS = {
    "Happy" : ["Walking on Sunshine", "Dancing Queen", 
        "Here Comes the Sun", "What a wonderful world", 
        "Beautiful Day", "Happy", "Rhythm and Blues", "Happy", "8TEEN", 
        "Good Life", "Mona Lisa", "Castle on the Hill", "Confident"],
    "Sad" : ["My heart will go on", "Candle in the wind", 
        "Marvin's room", "Redemption", "Driver's lisence", 
        "Heartbreak Anniversery", "Coaster", "Cold Blooded", "Ivy",
        "Find you", "Blue", "Bahamas Promises", "Alone"],
    "Angry" : ["Nonstop", "Rolling in the Deep", "Break Stuff", 
        "I'm Upset", "Worst behavior", "99 problems", 
        "I heard it through the grapevine", "Ex-factor", 
        "Irreplacable", "The Final Countdown", "IDGAF", 
        "Commitment Issues", "Shot for me"], 
    "Excited" : ["Can't stop the feeling", "Dynamite", 
        "Walking on Sunshine", "All Star", "I gotta Feeling", 
        "Twist and shout", "Superstar Sh*t", "Watermelon Sugar", 
        "Intentions", "One Thing", "Sugar", "Cool Kids", 
        "Can't Feel my Face" ],
    "Tired" : ["Socks", "babydoll", "Tired of Running", "Jaded", 
        "Furthest Thing", "Tried Our Best", "Apocolypse", 
        "never find u", "Are You Bored Yet?", "Blessed", "Streetcar", 
        "I'm tired", "Apocalypse"],
    "Stressed" : ["Changes", "Don't give up on me", "Stay", 
        "This City", "Do not Distrub", "One Man can change the world", 
        "Emotion", "Chanel", "Japanesse Denim", "Goodbyes", "Lie", 
        "White Ferrari", "Come Back to Earth"]
}  


class Spotify:
    """ Generates a spotify playlist based on the user's emotion.
    ...

    Attributes
    ----------
    emotion : string
        The user's current emotion.

    Methods
    -------
    select_song():
        Chooses a random song associated with the current emotion.
    make_playlist():
        Generates and directs user to spotify playlist based on selected song.
    """

    def __init__(self, emotion):
        """ Initializes spotify playlist maker.
            Args:
                emotion (string) : emotion to base playlist around
        """
        self.emotion = emotion

    def select_song(self):
        """ Selects a song associated with the user's emotion.
        """
        song_opts = EMOTIONAL_SONGS[self.emotion]  
        return random.choice(song_opts)

    def make_playlist(self, name):
        """ Generates and directs user to spotify playlist based on selected 
            song.
            Args:
                name (string) : User's name to incoporate into playlist name
        """
        song = self.select_song()

        scope = "playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
            client_id="81e6c74b51b54640a88ca4b4e40369d5",
            client_secret="149713aa148f48fd9e48c262e94516fd",
            redirect_uri="http://localhost:3000",))
        results = sp.search(q=song, type='track', limit=1)
        song_uri = results['tracks']['items'][0]['uri']

        # Create a new playlist
        playlist = sp.user_playlist_create(user="31sfpjpoeu7fn6qj34ervkv6hjum",
        name=f"{self.emotion} cookie baking songs for " + name, public=True)
        print(playlist['external_urls']['spotify'])

        recs = sp.recommendations(seed_tracks=[song_uri], limit=30)  

        #Add recommended songs to the playlist
        recommended_uris = [track['uri'] for track in recs['tracks']]
        recommended_uris.insert(0, song_uri)
        sp.playlist_add_items(playlist['id'], recommended_uris)

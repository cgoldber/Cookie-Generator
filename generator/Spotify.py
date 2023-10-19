import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random



class Spotify:
    
    
    # scope = "playlist-modify-public"
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def get_song(self, emotion):
        Happy_songs = ["Walking on Sunshine", "Dancing Queen", "Here Comes the Sun", "What a wonderful world", "Beautiful Day", "Happy", "Rhythm and Blues", "Happy", "8TEEN", "Good Life", "Mona Lisa", "Castle on the Hill", "Confident"] #13
        Sad_songs = ["My heart will go on", "Candle in the wind", "Marvin's room", "Redemption", "Driver's lisence", "Heartbreak Anniversery", "Coaster", "Cold Blooded", "Ivy","Find you", "Blue", "Bahamas Promises", "Alone"] #13
        Angry_songs = ["Nonstop", "Rolling in the Deep", "Break Stuff", "I'm Upset", "Worst behavior", "99 problems", "I heard it through the grapevine", "Ex-factor", "Irreplacable", "The Final Countdown", "IDGAF", "Commitment Issues", "Shot for me"] #13
        Excited_songs = ["Can't stop the feeling", "Dynamite", "Walking on Sunshine", "All Star", "I gotta Feeling", "Twist and shout", "Superstar Sh*t", "Watermelon Sugar", "Intentions", "One Thing", "Sugar", "Cool Kids", "Can't Feel my Face" ]#13
        Tired_songs = ["Socks", "babydoll", "Tired of Running", "Jaded", "Furthest Thing", "Tried Our Best", "Apocolypse", "never find u", "Are You Bored Yet?", "I love you", "Streetcar", "I'm tired", "Apocalypse"] #13
        Stressed_songs = ["Changes", "Don't give up on me", "Stay", "This City", "Do not Distrub", "One Man can change the world", "Emotion", "Chanel", "Japanesse Denim", "Goodbyes", "Lie", "White Ferrari", "Come Back to Earth"] #13
        Emotional_songs = {"Happy": Happy_songs, "Sad":Sad_songs, "Angry": Angry_songs, "Excited" : Excited_songs, "Tired" : Tired_songs, "Stressed": Stressed_songs }
            
        for key in Emotional_songs:
            if emotion == key:
                song = Emotional_songs[emotion]
                name = song[random.randint(0,12)]
                return name

    def make_playlist(self, song, emotion, name):
        scope = "playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id="81e6c74b51b54640a88ca4b4e40369d5",
            client_secret="149713aa148f48fd9e48c262e94516fd",
            redirect_uri="http://localhost:3000",))
        results = sp.search(q=song, type='track', limit=1)
        song_uri = results['tracks']['items'][0]['uri']

        # Step 5: Create a new playlist
        playlist = sp.user_playlist_create(user="31sfpjpoeu7fn6qj34ervkv6hjum", name=f"{emotion} cookie baking songs for " + name, public=True)
        print(playlist['external_urls']['spotify'])

        recommendations = sp.recommendations(seed_tracks=[song_uri], limit=30)  

        # Step 8: Add recommended songs to the playlist
        recommended_uris = [track['uri'] for track in recommendations['tracks']]
        recommended_uris.insert(0, song_uri)
        sp.playlist_add_items(playlist['id'], recommended_uris)
    

    # if __name__ == "__main__":
        
        # name_Person = input("Enter your name:  ")
        # Emotion_input = input("Pick an emotion: Happy, Sad, Angry, Excited, Tired, Stressed:  ")
        
        # emotion = Emotion_input
        
        # song = get_song(emotion)
        # print("This is the seed song " + song)
        # playlist = make_playlist(song, emotion, name_Person)
        




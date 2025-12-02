# Fichier : models.py

# Les 8 classes de modèle (DTOs)
class Genre:
    def __init__(self, id_genre=None, nom_genre=None):
        self.id_genre = id_genre
        self.nom_genre = nom_genre
        
class Subgenre:
    def __init__(self, id_subgenre=None, nom_subgenre=None, id_genre=None):
        self.id_subgenre = id_subgenre
        self.nom_subgenre = nom_subgenre
        self.id_genre = id_genre

class Artist:
    def __init__(self, id_artist=None, nom_artist=None):
        self.id_artist = id_artist
        self.nom_artist = nom_artist

class Album:
    def __init__(self, id_album=None, nom_album=None, date_sortie=None, id_artist=None):
        self.id_album = id_album
        self.nom_album = nom_album
        self.date_sortie = date_sortie
        self.id_artist = id_artist

class Track:
    def __init__(self, id_track=None, nom_track=None, duration_ms=None, track_popularity=None, id_album=None, track_href=None, uri=None):
        self.id_track = id_track
        self.nom_track = nom_track
        self.duration_ms = duration_ms
        self.track_popularity = track_popularity
        self.id_album = id_album
        self.track_href = track_href
        self.uri = uri

class AudioFeatures:
    def __init__(self, id_track=None, energy=None, tempo=None, danceability=None, loudness=None, liveness=None, valence=None, speechiness=None, acousticness=None, instrumentalness=None, key_musical=None, mode_musical=None, time_signature=None, analysis_url=None):
        self.id_track = id_track
        self.energy = energy
        self.tempo = tempo
        self.danceability = danceability
        self.loudness = loudness
        self.liveness = liveness
        self.valence = valence
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.key_musical = key_musical
        self.mode_musical = mode_musical
        self.time_signature = time_signature
        self.analysis_url = analysis_url

class Playlist:
    def __init__(self, id_playlist=None, nom_playlist=None, id_subgenre=None):
        self.id_playlist = id_playlist
        self.nom_playlist = nom_playlist
        self.id_subgenre = id_subgenre

class PlaylistTrack:
    def __init__(self, id_playlist=None, id_track=None):
        self.id_playlist = id_playlist
        self.id_track = id_track
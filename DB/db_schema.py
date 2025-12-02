# Fichier : db_schema.py

# Liste des tables à supprimer dans l'ordre inverse des dépendances (enfants avant parents)
DROP_TABLES_SQL = [
    "DROP TABLE sp_playlist_tracks",
    "DROP TABLE sp_playlists",
    "DROP TABLE sp_audio_features",
    "DROP TABLE sp_tracks",
    "DROP TABLE sp_albums",
    "DROP TABLE sp_artists",
    "DROP TABLE sp_subgenres",
    "DROP TABLE sp_genres",
]

# Script de création des tables (DDL)
CREATE_TABLES_SQL = """
-- 1. Table GENRES
CREATE TABLE sp_genres (
    id_genre NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom_genre VARCHAR2(100) NOT NULL UNIQUE
);

-- 2. Table SUBGENRES
CREATE TABLE sp_subgenres (
    id_subgenre NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom_subgenre VARCHAR2(100) NOT NULL UNIQUE,
    id_genre NUMBER NOT NULL,
    CONSTRAINT fk_sp_subgenre_genre 
        FOREIGN KEY (id_genre) 
        REFERENCES sp_genres(id_genre)
        ON DELETE CASCADE
);

-- 3. Table ARTISTS
CREATE TABLE sp_artists (
    id_artist NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nom_artist VARCHAR2(255) NOT NULL UNIQUE
);

-- 4. Table ALBUMS
CREATE TABLE sp_albums (
    id_album VARCHAR2(50) PRIMARY KEY,
    nom_album VARCHAR2(255) NOT NULL,
    date_sortie DATE,
    id_artist NUMBER NOT NULL,
    CONSTRAINT fk_sp_album_artist 
        FOREIGN KEY (id_artist) 
        REFERENCES sp_artists(id_artist)
        ON DELETE CASCADE
);

-- 5. Table TRACKS
CREATE TABLE sp_tracks (
    id_track VARCHAR2(50) PRIMARY KEY,
    track_name VARCHAR2(255) NOT NULL,
    track_href VARCHAR2(500),
    uri VARCHAR2(255) UNIQUE,
    duration_ms NUMBER,
    track_popularity NUMBER,
    id_album VARCHAR2(50) NOT NULL,
    CONSTRAINT fk_sp_track_album 
        FOREIGN KEY (id_album) 
        REFERENCES sp_albums(id_album)
        ON DELETE CASCADE
);

-- 6. Table AUDIO_FEATURES
CREATE TABLE sp_audio_features (
    id_track VARCHAR2(50) PRIMARY KEY,
    energy NUMBER(5,4),
    tempo NUMBER(7,3),
    danceability NUMBER(5,4),
    loudness NUMBER(6,3),
    liveness NUMBER(5,4),
    valence NUMBER(5,4),
    speechiness NUMBER(5,4),
    acousticness NUMBER(5,4),
    instrumentalness NUMBER(5,4),
    key_musical NUMBER,
    mode_musical NUMBER,
    time_signature NUMBER,
    analysis_url VARCHAR2(500),
    CONSTRAINT fk_sp_audio_track 
        FOREIGN KEY (id_track) 
        REFERENCES sp_tracks(id_track)
        ON DELETE CASCADE
);

-- 7. Table PLAYLISTS
CREATE TABLE sp_playlists (
    id_playlist VARCHAR2(50) PRIMARY KEY,
    nom_playlist VARCHAR2(255) NOT NULL,
    id_subgenre NUMBER,
    CONSTRAINT fk_sp_playlist_subgenre 
        FOREIGN KEY (id_subgenre) 
        REFERENCES sp_subgenres(id_subgenre)
        ON DELETE SET NULL
);

-- 8. Table PLAYLIST_TRACKS (table de liaison N:M)
CREATE TABLE sp_playlist_tracks (
    id_playlist VARCHAR2(50),
    id_track VARCHAR2(50),
    PRIMARY KEY (id_playlist, id_track),
    CONSTRAINT fk_sp_pt_playlist 
        FOREIGN KEY (id_playlist) 
        REFERENCES sp_playlists(id_playlist)
        ON DELETE CASCADE,
    CONSTRAINT fk_sp_pt_track 
        FOREIGN KEY (id_track) 
        REFERENCES sp_tracks(id_track)
        ON DELETE CASCADE
);
"""
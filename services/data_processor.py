# Fichier : data_processor.py

import pandas as pd
import re
import sys
from datetime import datetime
from configs import CSV_FILE_PATH

def extract_artists(artist_string):
    """
    Sépare les noms d'artistes dans une chaîne, nettoie les guillemets et met en minuscule.
    
    Args:
        artist_string: Chaîne contenant les noms d'artistes séparés par des virgules
        
    Returns:
        Liste des noms d'artistes nettoyés et en minuscules
    """
    if pd.isna(artist_string) or artist_string == '':
        return []
    
    # Nettoie les guillemets et espaces, puis met en minuscule
    artists = [re.sub(r'["\']', '', a).strip().lower() for a in str(artist_string).split(',')]
    # Filtre les chaînes vides
    return [a for a in artists if a]


def clean_column_name(col_name):
    """Nettoie les noms de colonnes (espaces, caractères spéciaux)."""
    return col_name.strip().lower()


def parse_date(date_str):
    """
    Parse les dates dans différents formats Spotify.
    Retourne une date au format YYYY-MM-DD ou None.
    """
    if pd.isna(date_str) or date_str == '':
        return None
    
    date_str = str(date_str).strip()
    
    # Format YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    
    # Format YYYY-MM
    if re.match(r'^\d{4}-\d{2}$', date_str):
        return f"{date_str}-01"
    
    # Format YYYY seulement
    if re.match(r'^\d{4}$', date_str):
        return f"{date_str}-01-01"
    
    return None


def preprocess_csv():
    """
    Lit le CSV, normalise et retourne un dictionnaire de DataFrames prêts pour l'insertion.
    
    Returns:
        dict: Dictionnaire contenant les DataFrames pour chaque table
    """
    # Lecture du CSV avec gestion d'erreurs
    try:
        df_raw = pd.read_csv(CSV_FILE_PATH, encoding='utf-8')
        print(f"✅ Fichier CSV chargé : {len(df_raw)} lignes")
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {CSV_FILE_PATH} n'a pas été trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV : {e}")
        sys.exit(1)

    print(f"🔄 Analyse et normalisation de {CSV_FILE_PATH}...")
    
    # Nettoyage des noms de colonnes
    df_raw.columns = [clean_column_name(col) for col in df_raw.columns]
    
    # Mapping des colonnes (au cas où il y a des variations)
    column_mapping = {
        'playlist_genre': 'nom_genre',
        'playlist_subgenre': 'nom_subgenre',
        'track_artist': 'artistes_collab',
        'track_album_id': 'id_album',
        'track_album_name': 'nom_album',
        'track_album_release_date': 'date_sortie',
        'track_id': 'id_track',
        'track_name': 'nom_track',
        'playlist_id': 'id_playlist',
        'playlist_name': 'nom_playlist',
        'key': 'key_musical',
        'mode': 'mode_musical',
        'time_signature': 'time_signature'
    }
    
    df_raw = df_raw.rename(columns=column_mapping)
    
    # Vérification des colonnes essentielles
    required_cols = ['nom_genre', 'nom_subgenre', 'artistes_collab', 'id_album', 
                     'nom_album', 'date_sortie', 'id_track', 'nom_track']
    missing_cols = [col for col in required_cols if col not in df_raw.columns]
    
    if missing_cols:
        print(f"⚠️ Colonnes manquantes : {missing_cols}")
        print(f"📋 Colonnes disponibles : {list(df_raw.columns)}")
    
    # --- 1. GENRES (sp_genres) ---
    print("📊 Extraction des genres...")
    genres_df = df_raw[['nom_genre']].dropna().drop_duplicates()
    genres_df['nom_genre'] = genres_df['nom_genre'].str.strip().str.lower()
    genres_df = genres_df[genres_df['nom_genre'] != ''].sort_values('nom_genre').reset_index(drop=True)
    print(f"   → {len(genres_df)} genres uniques")
    
    # --- 2. ARTISTES (sp_artists) ---
    print("🎤 Extraction des artistes...")
    all_artists = set()
    for artists_list in df_raw['artistes_collab'].apply(extract_artists):
        all_artists.update(artists_list)
    
    all_artists.discard('')  # Supprime les chaînes vides
    artists_df = pd.DataFrame(sorted(list(all_artists)), columns=['nom_artist'])
    print(f"   → {len(artists_df)} artistes uniques")
    
    # --- 3. SOUS-GENRES (sp_subgenres) ---
    print("🎵 Extraction des sous-genres...")
    subgenres_temp = df_raw[['nom_subgenre', 'nom_genre']].dropna().copy()
    subgenres_temp['nom_subgenre'] = subgenres_temp['nom_subgenre'].str.strip().str.lower()
    subgenres_temp['nom_genre'] = subgenres_temp['nom_genre'].str.strip().str.lower()
    
    # Suppression des doublons en gardant la première occurrence
    subgenres_df = subgenres_temp.drop_duplicates(subset=['nom_subgenre'], keep='first')
    subgenres_df = subgenres_df[
        (subgenres_df['nom_subgenre'] != '') & 
        (subgenres_df['nom_genre'] != '')
    ].reset_index(drop=True)
    print(f"   → {len(subgenres_df)} sous-genres uniques")
    
    # --- 4. ALBUMS (sp_albums) ---
    print("💿 Extraction des albums...")
    albums_temp = df_raw[['id_album', 'nom_album', 'date_sortie', 'artistes_collab']].dropna(subset=['id_album'])
    albums_temp = albums_temp.drop_duplicates(subset=['id_album'])
    
    # Conversion et nettoyage
    albums_temp['id_album'] = albums_temp['id_album'].astype(str).str.strip()
    albums_temp['nom_album'] = albums_temp['nom_album'].astype(str).str.strip()
    albums_temp['date_sortie'] = albums_temp['date_sortie'].apply(parse_date)
    
    # Extraction de l'artiste principal
    albums_temp['artiste_principal'] = albums_temp['artistes_collab'].apply(
        lambda x: extract_artists(x)[0] if extract_artists(x) else None
    )
    
    albums_df = albums_temp[['id_album', 'nom_album', 'date_sortie', 'artiste_principal']].copy()
    albums_df = albums_df[albums_df['id_album'] != ''].reset_index(drop=True)
    print(f"   → {len(albums_df)} albums uniques")
    
    # --- 5. PLAYLISTS (sp_playlists) ---
    print("📝 Extraction des playlists...")
    playlists_temp = df_raw[['id_playlist', 'nom_playlist', 'nom_subgenre']].dropna(subset=['id_playlist'])
    playlists_temp = playlists_temp.drop_duplicates(subset=['id_playlist'])
    
    # Conversion et nettoyage
    playlists_temp['id_playlist'] = playlists_temp['id_playlist'].astype(str).str.strip()
    playlists_temp['nom_playlist'] = playlists_temp['nom_playlist'].astype(str).str.strip()
    playlists_temp['nom_subgenre'] = playlists_temp['nom_subgenre'].str.strip().str.lower()
    
    playlists_df = playlists_temp[['id_playlist', 'nom_playlist', 'nom_subgenre']].copy()
    playlists_df = playlists_df[playlists_df['id_playlist'] != ''].reset_index(drop=True)
    print(f"   → {len(playlists_df)} playlists uniques")
    
    # --- 6. TRACKS (sp_tracks) ---
    print("🎶 Extraction des tracks...")
    tracks_cols = ['id_track', 'nom_track', 'duration_ms', 'track_popularity', 'id_album']
    tracks_temp = df_raw[tracks_cols].dropna(subset=['id_track'])
    tracks_temp = tracks_temp.drop_duplicates(subset=['id_track'])
    
    # Conversion des types
    tracks_temp['id_track'] = tracks_temp['id_track'].astype(str).str.strip()
    tracks_temp['id_album'] = tracks_temp['id_album'].astype(str).str.strip()
    tracks_temp['nom_track'] = tracks_temp['nom_track'].astype(str).str.strip()
    
    # Conversion numérique avec gestion d'erreurs
    tracks_temp['duration_ms'] = pd.to_numeric(tracks_temp['duration_ms'], errors='coerce').fillna(0).astype(int)
    tracks_temp['track_popularity'] = pd.to_numeric(tracks_temp['track_popularity'], errors='coerce').fillna(0).astype(int)
    
    tracks_df = tracks_temp.copy()
    tracks_df = tracks_df[tracks_df['id_track'] != ''].reset_index(drop=True)
    
    # Ajout de colonnes optionnelles
    tracks_df['track_href'] = None
    tracks_df['uri'] = None
    print(f"   → {len(tracks_df)} tracks uniques")
    
    # --- 7. AUDIO FEATURES (sp_audio_features) ---
    print("🎼 Extraction des audio features...")
    audio_cols = ['id_track', 'energy', 'tempo', 'danceability', 'loudness', 'liveness',
                  'valence', 'speechiness', 'acousticness', 'instrumentalness',
                  'key_musical', 'mode_musical', 'time_signature']
    
    # Vérifier quelles colonnes existent
    available_audio_cols = [col for col in audio_cols if col in df_raw.columns]
    
    if 'analysis_url' in df_raw.columns:
        available_audio_cols.append('analysis_url')
    
    audio_features_temp = df_raw[available_audio_cols].dropna(subset=['id_track'])
    audio_features_temp = audio_features_temp.drop_duplicates(subset=['id_track'])
    
    # Conversion des types
    audio_features_temp['id_track'] = audio_features_temp['id_track'].astype(str).str.strip()
    
    # Conversion des colonnes numériques
    numeric_cols = ['energy', 'tempo', 'danceability', 'loudness', 'liveness',
                    'valence', 'speechiness', 'acousticness', 'instrumentalness']
    
    for col in numeric_cols:
        if col in audio_features_temp.columns:
            audio_features_temp[col] = pd.to_numeric(audio_features_temp[col], errors='coerce')
    
    # Conversion des colonnes entières
    int_cols = ['key_musical', 'mode_musical', 'time_signature']
    for col in int_cols:
        if col in audio_features_temp.columns:
            audio_features_temp[col] = pd.to_numeric(audio_features_temp[col], errors='coerce').fillna(0).astype(int)
    
    audio_features_df = audio_features_temp.copy()
    audio_features_df = audio_features_df[audio_features_df['id_track'] != ''].reset_index(drop=True)
    print(f"   → {len(audio_features_df)} audio features")
    
    # --- 8. PLAYLIST TRACKS (sp_playlist_tracks) ---
    print("🔗 Extraction des relations playlist-tracks...")
    playlist_tracks_temp = df_raw[['id_playlist', 'id_track']].dropna()
    playlist_tracks_temp = playlist_tracks_temp.drop_duplicates()
    
    # Conversion des types
    playlist_tracks_temp['id_playlist'] = playlist_tracks_temp['id_playlist'].astype(str).str.strip()
    playlist_tracks_temp['id_track'] = playlist_tracks_temp['id_track'].astype(str).str.strip()
    
    playlist_tracks_df = playlist_tracks_temp.copy()
    playlist_tracks_df = playlist_tracks_df[
        (playlist_tracks_df['id_playlist'] != '') & 
        (playlist_tracks_df['id_track'] != '')
    ].reset_index(drop=True)
    print(f"   → {len(playlist_tracks_df)} relations playlist-track")
    
    print("\n✅ Normalisation terminée. 8 DataFrames créés.")
    
    # Résumé
    print("\n" + "="*50)
    print("RÉSUMÉ DES DONNÉES NORMALISÉES")
    print("="*50)
    summary = {
        'Genres': len(genres_df),
        'Sous-genres': len(subgenres_df),
        'Artistes': len(artists_df),
        'Albums': len(albums_df),
        'Playlists': len(playlists_df),
        'Tracks': len(tracks_df),
        'Audio Features': len(audio_features_df),
        'Relations Playlist-Track': len(playlist_tracks_df)
    }
    
    for entity, count in summary.items():
        print(f"  • {entity:<25} : {count:>6} enregistrements")
    print("="*50 + "\n")
    
    return {
        'sp_genres': genres_df,
        'sp_subgenres': subgenres_df,
        'sp_artists': artists_df,
        'sp_albums': albums_df,
        'sp_tracks': tracks_df,
        'sp_audio_features': audio_features_df,
        'sp_playlists': playlists_df,
        'sp_playlist_tracks': playlist_tracks_df
    }


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du module data_processor...")
    try:
        data = preprocess_csv()
        print("✅ Test réussi !")
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
"""
Module d'export XML pour les données Spotify.
Génère un fichier XML structuré à partir des données de la base Oracle.
"""

from lxml import etree
from pathlib import Path
from datetime import datetime
import sys

# Import de la configuration
try:
    from configs import XML_OUTPUT_PATH
except ImportError:
    XML_OUTPUT_PATH = "./data/output/spotify_data_export.xml"


def sanitize_xml_value(value):
    """
    Nettoie une valeur pour l'XML en gérant les valeurs None et les types spéciaux.
    
    Args:
        value: Valeur à nettoyer
        
    Returns:
        str: Valeur nettoyée en chaîne de caractères
    """
    if value is None or value == '':
        return ''
    
    # Convertir en chaîne
    value_str = str(value)
    
    # Remplacer les caractères problématiques
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;'
    }
    
    for old, new in replacements.items():
        value_str = value_str.replace(old, new)
    
    return value_str.strip()


def format_duration(duration_ms):
    """
    Convertit une durée en millisecondes en format MM:SS.
    
    Args:
        duration_ms: Durée en millisecondes
        
    Returns:
        str: Durée formatée (ex: "03:45")
    """
    if not duration_ms or duration_ms == 0:
        return "00:00"
    
    try:
        duration_ms = int(duration_ms)
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        return f"{minutes:02d}:{seconds:02d}"
    except:
        return "00:00"


def group_data_by_playlist(data_list):
    """
    Regroupe les données par playlist pour créer une structure hiérarchique.
    
    Args:
        data_list: Liste de dictionnaires contenant les données jointes
        
    Returns:
        dict: Données regroupées par playlist
    """
    playlists = {}
    
    for row in data_list:
        playlist_id = row.get('id_playlist', '')
        
        # Initialiser la playlist si elle n'existe pas
        if playlist_id not in playlists:
            playlists[playlist_id] = {
                'id': playlist_id,
                'nom': row.get('nom_playlist', ''),
                'genre': row.get('nom_genre', ''),
                'subgenre': row.get('nom_subgenre', ''),
                'tracks': []
            }
        
        # Ajouter la track à la playlist
        track = {
            'id_track': row.get('id_track', ''),
            'track_name': row.get('track_name', ''),
            'duration_ms': row.get('duration_ms', 0),
            'track_popularity': row.get('track_popularity', 0),
            'album': {
                'id_album': row.get('id_album', ''),
                'nom_album': row.get('nom_album', ''),
                'date_sortie': row.get('date_sortie', '')
            },
            'artist': {
                'nom_artist': row.get('artiste_principal', '')
            },
            'audio_features': {
                'energy': row.get('energy', ''),
                'tempo': row.get('tempo', ''),
                'danceability': row.get('danceability', ''),
                'loudness': row.get('loudness', ''),
                'valence': row.get('valence', ''),
                'liveness': row.get('liveness', ''),
                'speechiness': row.get('speechiness', ''),
                'acousticness': row.get('acousticness', ''),
                'instrumentalness': row.get('instrumentalness', '')
            }
        }
        
        playlists[playlist_id]['tracks'].append(track)
    
    return playlists


def create_xml_from_data(data_list, output_path=None):
    """
    Crée un fichier XML structuré à partir des données de la base.
    
    Args:
        data_list: Liste de dictionnaires contenant les données
        output_path: Chemin du fichier XML de sortie (optionnel)
        
    Returns:
        str: Chemin du fichier XML généré
    """
    if output_path is None:
        output_path = XML_OUTPUT_PATH
    
    # Créer le répertoire de sortie s'il n'existe pas
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔄 Génération du fichier XML...")
    print(f"📁 Destination : {output_path}")
    
    # Regrouper les données par playlist
    playlists_data = group_data_by_playlist(data_list)
    
    print(f" {len(playlists_data)} playlists à exporter")
    print(f"{len(data_list)} tracks au total")
        # Créer l'élément racine
    root = etree.Element("spotify_data")
    root.set("generated_at", datetime.now().isoformat())
    root.set("total_playlists", str(len(playlists_data)))
    root.set("total_tracks", str(len(data_list)))
    
    # Ajouter un commentaire
    comment = etree.Comment(" Données Spotify exportées depuis Oracle Database ")
    root.append(comment)
    
    # Créer l'élément playlists
    playlists_elem = etree.SubElement(root, "playlists")
    
    # Parcourir chaque playlist
    for playlist_id, playlist_data in sorted(playlists_data.items()):
        playlist_elem = etree.SubElement(playlists_elem, "playlist")
        playlist_elem.set("id", sanitize_xml_value(playlist_data['id']))
        
        # Informations de la playlist
        nom_elem = etree.SubElement(playlist_elem, "nom")
        nom_elem.text = sanitize_xml_value(playlist_data['nom'])
        
        genre_elem = etree.SubElement(playlist_elem, "genre")
        genre_elem.text = sanitize_xml_value(playlist_data['genre'])
        
        subgenre_elem = etree.SubElement(playlist_elem, "subgenre")
        subgenre_elem.text = sanitize_xml_value(playlist_data['subgenre'])
        
        # Élément tracks
        tracks_elem = etree.SubElement(playlist_elem, "tracks")
        tracks_elem.set("count", str(len(playlist_data['tracks'])))
        
        # Parcourir chaque track de la playlist
        for track in playlist_data['tracks']:
            track_elem = etree.SubElement(tracks_elem, "track")
            track_elem.set("id", sanitize_xml_value(track['id_track']))
            
            # Nom de la track
            track_name_elem = etree.SubElement(track_elem, "name")
            track_name_elem.text = sanitize_xml_value(track['track_name'])
            
            # Durée
            duration_elem = etree.SubElement(track_elem, "duration")
            duration_elem.set("ms", str(track['duration_ms']))
            duration_elem.text = format_duration(track['duration_ms'])
            
            # Popularité
            popularity_elem = etree.SubElement(track_elem, "popularity")
            popularity_elem.text = str(track['track_popularity'])
            
            # Album
            album_elem = etree.SubElement(track_elem, "album")
            album_elem.set("id", sanitize_xml_value(track['album']['id_album']))
            
            album_name_elem = etree.SubElement(album_elem, "name")
            album_name_elem.text = sanitize_xml_value(track['album']['nom_album'])
            
            if track['album']['date_sortie']:
                album_date_elem = etree.SubElement(album_elem, "release_date")
                album_date_elem.text = sanitize_xml_value(track['album']['date_sortie'])
            
            # Artiste
            artist_elem = etree.SubElement(track_elem, "artist")
            artist_name_elem = etree.SubElement(artist_elem, "name")
            artist_name_elem.text = sanitize_xml_value(track['artist']['nom_artist'])
            
            # Audio features (si disponibles)
            audio_feat = track['audio_features']
            if any(audio_feat.values()):
                audio_elem = etree.SubElement(track_elem, "audio_features")
                
                if audio_feat['energy']:
                    energy_elem = etree.SubElement(audio_elem, "energy")
                    energy_elem.text = str(audio_feat['energy'])
                
                if audio_feat['tempo']:
                    tempo_elem = etree.SubElement(audio_elem, "tempo")
                    tempo_elem.text = str(audio_feat['tempo'])
                
                if audio_feat['danceability']:
                    dance_elem = etree.SubElement(audio_elem, "danceability")
                    dance_elem.text = str(audio_feat['danceability'])
                
                if audio_feat['loudness']:
                    loud_elem = etree.SubElement(audio_elem, "loudness")
                    loud_elem.text = str(audio_feat['loudness'])
                
                if audio_feat['valence']:
                    valence_elem = etree.SubElement(audio_elem, "valence")
                    valence_elem.text = str(audio_feat['valence'])
    
    # Créer l'arbre XML
    tree = etree.ElementTree(root)
    
    # Écrire le fichier avec une mise en forme propre
    tree.write(
        str(output_file),
        encoding='utf-8',
        xml_declaration=True,
        pretty_print=True
    )
    
    # Calculer la taille du fichier
    file_size = output_file.stat().st_size
    file_size_kb = file_size / 1024
    
    print(f"\n Fichier XML généré avec succès !")
    print(f" Fichier : {output_path}")
    print(f" Taille : {file_size_kb:.2f} KB")
    print(f" Structure :")
    print(f"   • {len(playlists_data)} playlists")
    print(f"   • {len(data_list)} tracks")
    
    return str(output_file)


def export_to_xml(data_list, output_path=None):
    """
    Fonction principale d'export XML.
    Point d'entrée pour le module.
    
    Args:
        data_list: Liste de dictionnaires contenant les données
        output_path: Chemin du fichier de sortie (optionnel)
        
    Returns:
        str: Chemin du fichier XML généré
    """
    try:
        if not data_list:
            print("⚠️  Aucune donnée à exporter.")
            return None
        
        return create_xml_from_data(data_list, output_path)
    
    except Exception as e:
        print(f" Erreur lors de l'export XML : {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_xml_structure(xml_file):
    """
    Valide que le fichier XML est bien formé.
    
    Args:
        xml_file: Chemin du fichier XML
        
    Returns:
        bool: True si le XML est valide, False sinon
    """
    try:
        tree = etree.parse(xml_file)
        print(f" Le fichier XML est bien formé.")
        return True
    except etree.XMLSyntaxError as e:
        print(f" Erreur de syntaxe XML : {e}")
        return False
    except Exception as e:
        print(f" Erreur lors de la validation : {e}")
        return False


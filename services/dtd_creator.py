"""
Module de création de DTD pour les données Spotify.
Génère une DTD (Document Type Definition) décrivant la structure du XML.
"""

from pathlib import Path
from datetime import datetime

from configs.config import DTD_PATH, XML_OUTPUT_PATH, DTD_DOCUMENTATION_PATH


def create_spotify_dtd(output_path=None):
    """
    Crée un fichier DTD pour valider la structure du XML Spotify.
    
    Args:
        output_path: Chemin du fichier DTD de sortie (optionnel)
        
    Returns:
        str: Chemin du fichier DTD généré
    """
    if output_path is None:
        output_path = DTD_PATH
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🔄 Génération du fichier DTD...")
    print(f"📁 Destination : {output_path}")
    
    # Contenu de la DTD
    dtd_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
    DTD pour les données Spotify
    Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    Structure :
    - spotify_data (racine)
      └─ playlists
          └─ playlist (multiple)
              ├─ nom
              ├─ genre
              ├─ subgenre
              └─ tracks
                  └─ track (multiple)
                      ├─ name
                      ├─ duration
                      ├─ popularity
                      ├─ album
                      │   ├─ name
                      │   └─ release_date (optionnel)
                      ├─ artist
                      │   └─ name
                      └─ audio_features (optionnel)
                          ├─ energy
                          ├─ tempo
                          ├─ danceability
                          ├─ loudness
                          └─ valence
-->

<!-- ========================================================================== -->
<!-- ÉLÉMENT RACINE                                                             -->
<!-- ========================================================================== -->

<!ELEMENT spotify_data (playlists)>
<!ATTLIST spotify_data
    generated_at    CDATA #REQUIRED
    total_playlists CDATA #REQUIRED
    total_tracks    CDATA #REQUIRED
>

<!-- ========================================================================== -->
<!-- PLAYLISTS                                                                  -->
<!-- ========================================================================== -->

<!ELEMENT playlists (playlist+)>

<!ELEMENT playlist (nom, genre, subgenre, tracks)>
<!ATTLIST playlist
    id CDATA #REQUIRED
>

<!ELEMENT nom (#PCDATA)>
<!ELEMENT genre (#PCDATA)>
<!ELEMENT subgenre (#PCDATA)>

<!-- ========================================================================== -->
<!-- TRACKS                                                                     -->
<!-- ========================================================================== -->

<!ELEMENT tracks (track*)>
<!ATTLIST tracks
    count CDATA #REQUIRED
>

<!ELEMENT track (name, duration, popularity, album, artist, audio_features?)>
<!ATTLIST track
    id CDATA #REQUIRED
>

<!ELEMENT name (#PCDATA)>
<!ELEMENT duration (#PCDATA)>
<!ATTLIST duration
    ms CDATA #REQUIRED
>

<!ELEMENT popularity (#PCDATA)>

<!-- ========================================================================== -->
<!-- ALBUM                                                                      -->
<!-- ========================================================================== -->

<!ELEMENT album (name, release_date?)>
<!ATTLIST album
    id CDATA #REQUIRED
>

<!ELEMENT release_date (#PCDATA)>

<!-- ========================================================================== -->
<!-- ARTIST                                                                     -->
<!-- ========================================================================== -->

<!ELEMENT artist (name)>

<!-- ========================================================================== -->
<!-- AUDIO FEATURES                                                             -->
<!-- ========================================================================== -->

<!ELEMENT audio_features (energy?, tempo?, danceability?, loudness?, valence?, liveness?, speechiness?, acousticness?, instrumentalness?)>

<!ELEMENT energy (#PCDATA)>
<!ELEMENT tempo (#PCDATA)>
<!ELEMENT danceability (#PCDATA)>
<!ELEMENT loudness (#PCDATA)>
<!ELEMENT valence (#PCDATA)>
<!ELEMENT liveness (#PCDATA)>
<!ELEMENT speechiness (#PCDATA)>
<!ELEMENT acousticness (#PCDATA)>
<!ELEMENT instrumentalness (#PCDATA)>
"""
    
    # Écrire le fichier
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dtd_content)
        
        # Calculer la taille
        file_size = output_file.stat().st_size
        file_size_kb = file_size / 1024
        
        print(f"\n✅ Fichier DTD généré avec succès !")
        print(f"📄 Fichier : {output_path}")
        print(f"📊 Taille : {file_size_kb:.2f} KB")
        
        return str(output_file)
    
    except Exception as e:
        print(f"❌ Erreur lors de la création de la DTD : {e}")
        import traceback
        traceback.print_exc()
        return None


def print_dtd_info():
    """
    Affiche les informations sur la structure de la DTD.
    """
    print("\n📋 STRUCTURE DE LA DTD SPOTIFY")
    print("="*70)
    print("""
Élément racine :
  • spotify_data
    - Attributs : generated_at, total_playlists, total_tracks

Hiérarchie complète :
  spotify_data
    └─ playlists
        └─ playlist (+) [id]
            ├─ nom (texte)
            ├─ genre (texte)
            ├─ subgenre (texte)
            └─ tracks [count]
                └─ track (*) [id]
                    ├─ name (texte)
                    ├─ duration (texte) [ms]
                    ├─ popularity (texte)
                    ├─ album [id]
                    │   ├─ name (texte)
                    │   └─ release_date (texte, optionnel)
                    ├─ artist
                    │   └─ name (texte)
                    └─ audio_features (optionnel)
                        ├─ energy (texte, optionnel)
                        ├─ tempo (texte, optionnel)
                        ├─ danceability (texte, optionnel)
                        ├─ loudness (texte, optionnel)
                        ├─ valence (texte, optionnel)
                        ├─ liveness (texte, optionnel)
                        ├─ speechiness (texte, optionnel)
                        ├─ acousticness (texte, optionnel)
                        └─ instrumentalness (texte, optionnel)

Légende :
  (+) = Un ou plusieurs (au moins 1)
  (*) = Zéro ou plusieurs
  (?) = Optionnel (0 ou 1)
  [attr] = Attribut obligatoire
  (texte) = Contenu textuel (#PCDATA)
    """)


def add_dtd_reference_to_xml(xml_file, dtd_file):
    """
    Ajoute une référence DTD au début d'un fichier XML existant.
    
    Args:
        xml_file: Chemin du fichier XML
        dtd_file: Chemin du fichier DTD
        
    Returns:
        bool: True si succès, False sinon
    """
    try:
        xml_path = Path(xml_file)
        dtd_path = Path(dtd_file)
        
        # Calculer le chemin relatif
        dtd_relative = dtd_path.name  # Juste le nom si dans le même dossier
        
        # Lire le XML
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Vérifier si la référence DTD existe déjà
        if '<!DOCTYPE' in xml_content:
            print("ℹ️  Le fichier XML contient déjà une référence DTD.")
            return True
        
        # Ajouter la référence DTD après la déclaration XML
        lines = xml_content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            # Ajouter après la déclaration <?xml...?>
            if i == 0 and line.strip().startswith('<?xml'):
                new_lines.append(f'<!DOCTYPE spotify_data SYSTEM "{dtd_relative}">')
        
        # Écrire le nouveau contenu
        new_content = '\n'.join(new_lines)
        
        # Sauvegarder
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Référence DTD ajoutée au fichier XML")
        print(f"   <!DOCTYPE spotify_data SYSTEM \"{dtd_relative}\">")
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la référence DTD : {e}")
        return False


def generate_dtd_documentation(output_path=None):
    """
    Génère une documentation détaillée de la DTD en format texte.
    
    Args:
        output_path: Chemin du fichier de documentation (optionnel)
    """
    if output_path is None:
        output_path = DTD_DOCUMENTATION_PATH
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    doc_content = f"""╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                   DOCUMENTATION DTD - SPOTIFY DATA                        ║
║                   Générée le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝


📋 DESCRIPTION GÉNÉRALE
═══════════════════════════════════════════════════════════════════════════

La DTD (Document Type Definition) définit la structure valide du fichier
XML contenant les données Spotify exportées depuis Oracle Database.


📐 STRUCTURE HIÉRARCHIQUE
═══════════════════════════════════════════════════════════════════════════

spotify_data (racine)
  │
  └─── playlists
         │
         └─── playlist (1 à n)
                ├─── nom
                ├─── genre
                ├─── subgenre
                └─── tracks
                       │
                       └─── track (0 à n)
                              ├─── name
                              ├─── duration
                              ├─── popularity
                              ├─── album
                              │      ├─── name
                              │      └─── release_date (optionnel)
                              ├─── artist
                              │      └─── name
                              └─── audio_features (optionnel)
                                     ├─── energy (optionnel)
                                     ├─── tempo (optionnel)
                                     ├─── danceability (optionnel)
                                     ├─── loudness (optionnel)
                                     ├─── valence (optionnel)
                                     ├─── liveness (optionnel)
                                     ├─── speechiness (optionnel)
                                     ├─── acousticness (optionnel)
                                     └─── instrumentalness (optionnel)


📦 ÉLÉMENTS DÉTAILLÉS
═══════════════════════════════════════════════════════════════════════════

1. SPOTIFY_DATA (Racine)
───────────────────────────────────────────────────────────────────────────
   Type        : Élément racine du document
   Contenu     : (playlists)
   Attributs   :
     • generated_at    : Date/heure de génération (REQUIS)
     • total_playlists : Nombre total de playlists (REQUIS)
     • total_tracks    : Nombre total de tracks (REQUIS)
   
   Exemple :
   <spotify_data generated_at="2024-01-20T15:30:00" 
                 total_playlists="72" 
                 total_tracks="1670">


2. PLAYLISTS
───────────────────────────────────────────────────────────────────────────
   Type        : Conteneur de playlists
   Contenu     : (playlist+) - Au moins une playlist
   Attributs   : Aucun


3. PLAYLIST
───────────────────────────────────────────────────────────────────────────
   Type        : Représente une playlist Spotify
   Contenu     : (nom, genre, subgenre, tracks)
   Attributs   :
     • id : Identifiant Spotify de la playlist (REQUIS)
   
   Exemple :
   <playlist id="37i9dQZF1DX0XUsuxWHRQd">


4. NOM, GENRE, SUBGENRE
───────────────────────────────────────────────────────────────────────────
   Type        : Données textuelles
   Contenu     : #PCDATA (texte simple)
   Attributs   : Aucun
   
   Exemples :
   <nom>RapCaviar</nom>
   <genre>rap</genre>
   <subgenre>hip hop</subgenre>


5. TRACKS
───────────────────────────────────────────────────────────────────────────
   Type        : Conteneur de tracks
   Contenu     : (track*) - Zéro ou plusieurs tracks
   Attributs   :
     • count : Nombre de tracks dans la playlist (REQUIS)
   
   Exemple :
   <tracks count="25">


6. TRACK
───────────────────────────────────────────────────────────────────────────
   Type        : Représente une piste musicale
   Contenu     : (name, duration, popularity, album, artist, audio_features?)
   Attributs   :
     • id : Identifiant Spotify de la track (REQUIS)
   
   Note : audio_features est optionnel (?)
   
   Exemple :
   <track id="3KkXRkHbMCARz0aVfEt68P">


7. NAME (Track)
───────────────────────────────────────────────────────────────────────────
   Type        : Nom de la track
   Contenu     : #PCDATA
   Attributs   : Aucun
   
   Exemple :
   <name>Example Song</name>


8. DURATION
───────────────────────────────────────────────────────────────────────────
   Type        : Durée de la track
   Contenu     : #PCDATA (format MM:SS)
   Attributs   :
     • ms : Durée en millisecondes (REQUIS)
   
   Exemple :
   <duration ms="210000">03:30</duration>


9. POPULARITY
───────────────────────────────────────────────────────────────────────────
   Type        : Score de popularité
   Contenu     : #PCDATA (nombre 0-100)
   Attributs   : Aucun
   
   Exemple :
   <popularity>85</popularity>


10. ALBUM
───────────────────────────────────────────────────────────────────────────
   Type        : Informations sur l'album
   Contenu     : (name, release_date?)
   Attributs   :
     • id : Identifiant Spotify de l'album (REQUIS)
   
   Note : release_date est optionnel
   
   Exemple :
   <album id="2ODvWsOgouMbaA5xf0RkJe">
     <name>Example Album</name>
     <release_date>2023-01-15</release_date>
   </album>


11. ARTIST
───────────────────────────────────────────────────────────────────────────
   Type        : Informations sur l'artiste
   Contenu     : (name)
   Attributs   : Aucun
   
   Exemple :
   <artist>
     <name>Example Artist</name>
   </artist>


12. AUDIO_FEATURES
───────────────────────────────────────────────────────────────────────────
   Type        : Caractéristiques audio (OPTIONNEL)
   Contenu     : (energy?, tempo?, danceability?, loudness?, valence?, 
                  liveness?, speechiness?, acousticness?, instrumentalness?)
   Attributs   : Aucun
   
   Note : Tous les sous-éléments sont optionnels
   
   Exemple :
   <audio_features>
     <energy>0.8</energy>
     <tempo>120.5</tempo>
     <danceability>0.7</danceability>
     <loudness>-5.2</loudness>
     <valence>0.6</valence>
   </audio_features>


13. CARACTÉRISTIQUES AUDIO (Détails)
───────────────────────────────────────────────────────────────────────────
   Tous les éléments suivants :
     • energy, tempo, danceability, loudness, valence,
       liveness, speechiness, acousticness, instrumentalness
   
   Type        : Valeurs numériques
   Contenu     : #PCDATA
   Attributs   : Aucun
   Optionnel   : Oui (peuvent être absents)


🔤 NOTATION DTD
═══════════════════════════════════════════════════════════════════════════

Symboles utilisés :
   +  = Un ou plusieurs (1..n)
   *  = Zéro ou plusieurs (0..n)
   ?  = Optionnel (0 ou 1)
   |  = Choix (OU)
   ,  = Séquence (ordre obligatoire)
   
Attributs :
   #REQUIRED   = Obligatoire
   #IMPLIED    = Optionnel
   #FIXED      = Valeur fixe
   CDATA       = Chaîne de caractères


✅ RÈGLES DE VALIDATION
═══════════════════════════════════════════════════════════════════════════

1. La racine doit être <spotify_data>
2. Il doit y avoir au moins une <playlist>
3. Chaque playlist doit avoir : nom, genre, subgenre, tracks
4. Les IDs (playlist, track, album) sont obligatoires
5. Chaque track doit avoir : name, duration, popularity, album, artist
6. audio_features est optionnel pour chaque track
7. release_date est optionnel pour chaque album
8. L'ordre des éléments doit être respecté


❌ ERREURS COURANTES
═══════════════════════════════════════════════════════════════════════════

1. Playlist sans tracks
   → Erreur : tracks est obligatoire même si vide
   
2. Ordre des éléments incorrect
   → Erreur : Respecter (nom, genre, subgenre, tracks)
   
3. Attribut id manquant
   → Erreur : id est obligatoire pour playlist, track, album
   
4. Élément audio_features vide mais présent
   → OK : audio_features peut être vide ou absent


📝 EXEMPLE COMPLET VALIDE
═══════════════════════════════════════════════════════════════════════════

<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE spotify_data SYSTEM "spotify_data.dtd">
<spotify_data generated_at="2024-01-20T15:30:00" 
              total_playlists="1" 
              total_tracks="1">
  <playlists>
    <playlist id="37i9dQZF1DX0XUsuxWHRQd">
      <nom>RapCaviar</nom>
      <genre>rap</genre>
      <subgenre>hip hop</subgenre>
      <tracks count="1">
        <track id="3KkXRkHbMCARz0aVfEt68P">
          <name>Example Song</name>
          <duration ms="210000">03:30</duration>
          <popularity>85</popularity>
          <album id="2ODvWsOgouMbaA5xf0RkJe">
            <name>Example Album</name>
            <release_date>2023-01-15</release_date>
          </album>
          <artist>
            <name>Example Artist</name>
          </artist>
          <audio_features>
            <energy>0.8</energy>
            <tempo>120.5</tempo>
            <danceability>0.7</danceability>
            <loudness>-5.2</loudness>
            <valence>0.6</valence>
          </audio_features>
        </track>
      </tracks>
    </playlist>
  </playlists>
</spotify_data>


═══════════════════════════════════════════════════════════════════════════
Fin de la documentation
═══════════════════════════════════════════════════════════════════════════
"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"\n✅ Documentation DTD générée : {output_path}")
        return str(output_file)
    
    except Exception as e:
        print(f"❌ Erreur lors de la génération de la documentation : {e}")
        return None


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module dtd_creator")
    print("="*70)
    
    # Créer la DTD
    dtd_file = create_spotify_dtd(DTD_PATH)
    
    if dtd_file:
        print("\n✅ Test réussi !")
        print_dtd_info()
        
        # Générer la documentation
        generate_dtd_documentation(DTD_DOCUMENTATION_PATH)
    else:
        print("\n❌ Test échoué.")
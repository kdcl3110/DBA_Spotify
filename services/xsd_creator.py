
"""
Module de création de schéma XSD pour les données Spotify.
Génère un schéma XML Schema Definition (XSD) décrivant la structure du XML Spotify.
"""

from pathlib import Path
from lxml import etree


def create_spotify_xsd(xsd_file="./data/output/spotify_data.xsd"):
    """
    Crée un fichier XSD définissant la structure du XML Spotify.

    Args:
        xsd_file: Chemin du fichier XSD à créer

    Returns:
        bool: True si succès, False sinon
    """
    print(f"\n📋 Création du schéma XSD...")
    print(f"📄 Fichier de sortie : {xsd_file}")

    try:
        # Namespace XSD
        XS = "http://www.w3.org/2001/XMLSchema"
        NSMAP = {'xs': XS}

        # Créer l'élément racine du schéma
        schema = etree.Element(
            f"{{{XS}}}schema",
            nsmap=NSMAP,
            version="1.0"
        )

        # ===== Élément racine spotify_data =====
        spotify_data_element = etree.SubElement(schema, f"{{{XS}}}element", name="spotify_data")
        spotify_data_complex = etree.SubElement(spotify_data_element, f"{{{XS}}}complexType")
        spotify_data_sequence = etree.SubElement(spotify_data_complex, f"{{{XS}}}sequence")

        # Commentaire dans le XML
        comment_element = etree.SubElement(spotify_data_sequence, f"{{{XS}}}element", name="comment", minOccurs="0")
        comment_type = etree.SubElement(comment_element, f"{{{XS}}}simpleType")
        etree.SubElement(comment_type, f"{{{XS}}}restriction", base="xs:string")

        # Élément playlists
        etree.SubElement(spotify_data_sequence, f"{{{XS}}}element", ref="playlists")

        # Attributs de spotify_data
        etree.SubElement(spotify_data_complex, f"{{{XS}}}attribute", name="generated_at", type="xs:string", use="required")
        etree.SubElement(spotify_data_complex, f"{{{XS}}}attribute", name="total_playlists", type="xs:integer", use="required")
        etree.SubElement(spotify_data_complex, f"{{{XS}}}attribute", name="total_tracks", type="xs:integer", use="required")

        # ===== Élément playlists =====
        playlists_element = etree.SubElement(schema, f"{{{XS}}}element", name="playlists")
        playlists_complex = etree.SubElement(playlists_element, f"{{{XS}}}complexType")
        playlists_sequence = etree.SubElement(playlists_complex, f"{{{XS}}}sequence")
        etree.SubElement(playlists_sequence, f"{{{XS}}}element", ref="playlist", minOccurs="0", maxOccurs="unbounded")

        # ===== Élément playlist =====
        playlist_element = etree.SubElement(schema, f"{{{XS}}}element", name="playlist")
        playlist_complex = etree.SubElement(playlist_element, f"{{{XS}}}complexType")
        playlist_sequence = etree.SubElement(playlist_complex, f"{{{XS}}}sequence")

        # Éléments de playlist
        etree.SubElement(playlist_sequence, f"{{{XS}}}element", name="nom", type="xs:string")
        etree.SubElement(playlist_sequence, f"{{{XS}}}element", name="genre", type="xs:string")
        etree.SubElement(playlist_sequence, f"{{{XS}}}element", name="subgenre", type="xs:string")
        etree.SubElement(playlist_sequence, f"{{{XS}}}element", ref="tracks")

        # Attribut id de playlist
        etree.SubElement(playlist_complex, f"{{{XS}}}attribute", name="id", type="xs:string", use="required")

        # ===== Élément tracks =====
        tracks_element = etree.SubElement(schema, f"{{{XS}}}element", name="tracks")
        tracks_complex = etree.SubElement(tracks_element, f"{{{XS}}}complexType")
        tracks_sequence = etree.SubElement(tracks_complex, f"{{{XS}}}sequence")
        etree.SubElement(tracks_sequence, f"{{{XS}}}element", ref="track", minOccurs="0", maxOccurs="unbounded")

        # Attribut count de tracks
        etree.SubElement(tracks_complex, f"{{{XS}}}attribute", name="count", type="xs:integer", use="required")

        # ===== Élément track =====
        track_element = etree.SubElement(schema, f"{{{XS}}}element", name="track")
        track_complex = etree.SubElement(track_element, f"{{{XS}}}complexType")
        track_sequence = etree.SubElement(track_complex, f"{{{XS}}}sequence")

        # Éléments de track
        etree.SubElement(track_sequence, f"{{{XS}}}element", name="name", type="xs:string")
        etree.SubElement(track_sequence, f"{{{XS}}}element", ref="duration")
        etree.SubElement(track_sequence, f"{{{XS}}}element", name="popularity", type="xs:integer")
        etree.SubElement(track_sequence, f"{{{XS}}}element", ref="album")
        etree.SubElement(track_sequence, f"{{{XS}}}element", ref="artist")
        etree.SubElement(track_sequence, f"{{{XS}}}element", ref="audio_features")

        # Attribut id de track
        etree.SubElement(track_complex, f"{{{XS}}}attribute", name="id", type="xs:string", use="required")

        # ===== Élément duration =====
        duration_element = etree.SubElement(schema, f"{{{XS}}}element", name="duration")
        duration_complex = etree.SubElement(duration_element, f"{{{XS}}}complexType")
        duration_simple = etree.SubElement(duration_complex, f"{{{XS}}}simpleContent")
        duration_extension = etree.SubElement(duration_simple, f"{{{XS}}}extension", base="xs:string")
        etree.SubElement(duration_extension, f"{{{XS}}}attribute", name="ms", type="xs:integer", use="required")

        # ===== Élément album =====
        album_element = etree.SubElement(schema, f"{{{XS}}}element", name="album")
        album_complex = etree.SubElement(album_element, f"{{{XS}}}complexType")
        album_sequence = etree.SubElement(album_complex, f"{{{XS}}}sequence")
        etree.SubElement(album_sequence, f"{{{XS}}}element", name="name", type="xs:string")
        etree.SubElement(album_sequence, f"{{{XS}}}element", name="release_date", type="xs:string")
        etree.SubElement(album_complex, f"{{{XS}}}attribute", name="id", type="xs:string", use="required")

        # ===== Élément artist =====
        artist_element = etree.SubElement(schema, f"{{{XS}}}element", name="artist")
        artist_complex = etree.SubElement(artist_element, f"{{{XS}}}complexType")
        artist_sequence = etree.SubElement(artist_complex, f"{{{XS}}}sequence")
        etree.SubElement(artist_sequence, f"{{{XS}}}element", name="name", type="xs:string")

        # ===== Élément audio_features =====
        audio_features_element = etree.SubElement(schema, f"{{{XS}}}element", name="audio_features")
        audio_features_complex = etree.SubElement(audio_features_element, f"{{{XS}}}complexType")
        audio_features_sequence = etree.SubElement(audio_features_complex, f"{{{XS}}}sequence")

        # Types décimaux pour les caractéristiques audio
        etree.SubElement(audio_features_sequence, f"{{{XS}}}element", name="energy", type="xs:decimal")
        etree.SubElement(audio_features_sequence, f"{{{XS}}}element", name="tempo", type="xs:decimal")
        etree.SubElement(audio_features_sequence, f"{{{XS}}}element", name="danceability", type="xs:decimal")
        etree.SubElement(audio_features_sequence, f"{{{XS}}}element", name="loudness", type="xs:decimal")
        etree.SubElement(audio_features_sequence, f"{{{XS}}}element", name="valence", type="xs:decimal")

        # Créer l'arbre et sauvegarder
        tree = etree.ElementTree(schema)

        # Écrire le fichier avec une belle indentation
        with open(xsd_file, 'wb') as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        print(f"✅ Schéma XSD créé avec succès !")
        print(f"📋 Fichier : {xsd_file}")

        # Afficher des statistiques
        print_xsd_info(xsd_file)

        return True

    except Exception as e:
        print(f"\n❌ Erreur lors de la création du schéma XSD : {e}")
        import traceback
        traceback.print_exc()
        return False


def print_xsd_info(xsd_file):
    """
    Affiche des informations sur le schéma XSD créé.

    Args:
        xsd_file: Chemin du fichier XSD
    """
    try:
        tree = etree.parse(xsd_file)
        root = tree.getroot()

        # Namespace XSD
        ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}

        # Compter les éléments définis
        elements = root.findall('.//xs:element[@name]', ns)
        complex_types = root.findall('.//xs:complexType', ns)
        attributes = root.findall('.//xs:attribute', ns)

        print(f"\n📊 Statistiques du schéma XSD :")
        print(f"   • Éléments définis    : {len(elements)}")
        print(f"   • Types complexes     : {len(complex_types)}")
        print(f"   • Attributs           : {len(attributes)}")

        print(f"\n📋 Éléments principaux :")
        for elem in elements:
            name = elem.get('name')
            elem_type = elem.get('type', 'complexType')
            print(f"   • {name} ({elem_type})")

        # Taille du fichier
        file_size = Path(xsd_file).stat().st_size
        print(f"\n📦 Taille du fichier : {file_size} bytes ({file_size/1024:.2f} KB)")

    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des informations : {e}")


def generate_xsd_documentation(xsd_file, doc_file="./data/output/XSD_DOCUMENTATION.txt"):
    """
    Génère une documentation textuelle du schéma XSD.

    Args:
        xsd_file: Chemin du fichier XSD
        doc_file: Chemin du fichier de documentation

    Returns:
        bool: True si succès
    """
    print(f"\n📝 Génération de la documentation XSD...")

    try:
        doc_content = []
        doc_content.append("=" * 80)
        doc_content.append("DOCUMENTATION DU SCHÉMA XSD - Données Spotify")
        doc_content.append("=" * 80)
        doc_content.append("")
        doc_content.append("Ce schéma XSD définit la structure et les types de données pour")
        doc_content.append("l'export XML des données Spotify.")
        doc_content.append("")
        doc_content.append("=" * 80)
        doc_content.append("STRUCTURE HIÉRARCHIQUE")
        doc_content.append("=" * 80)
        doc_content.append("")
        doc_content.append("spotify_data (@generated_at, @total_playlists, @total_tracks)")
        doc_content.append("│")
        doc_content.append("└── playlists")
        doc_content.append("    │")
        doc_content.append("    └── playlist* (@id)")
        doc_content.append("        ├── nom (string)")
        doc_content.append("        ├── genre (string)")
        doc_content.append("        ├── subgenre (string)")
        doc_content.append("        │")
        doc_content.append("        └── tracks (@count)")
        doc_content.append("            │")
        doc_content.append("            └── track* (@id)")
        doc_content.append("                ├── name (string)")
        doc_content.append("                ├── duration (@ms) (string)")
        doc_content.append("                ├── popularity (integer)")
        doc_content.append("                ├── album (@id)")
        doc_content.append("                │   ├── name (string)")
        doc_content.append("                │   └── release_date (string)")
        doc_content.append("                ├── artist")
        doc_content.append("                │   └── name (string)")
        doc_content.append("                └── audio_features")
        doc_content.append("                    ├── energy (decimal)")
        doc_content.append("                    ├── tempo (decimal)")
        doc_content.append("                    ├── danceability (decimal)")
        doc_content.append("                    ├── loudness (decimal)")
        doc_content.append("                    └── valence (decimal)")
        doc_content.append("")
        doc_content.append("Légende : * = peut se répéter (0 à n occurrences)")
        doc_content.append("          @ = attribut")
        doc_content.append("")
        doc_content.append("=" * 80)
        doc_content.append("DÉFINITIONS DES TYPES")
        doc_content.append("=" * 80)
        doc_content.append("")
        doc_content.append("Types de données utilisés :")
        doc_content.append("  • xs:string  : Chaîne de caractères")
        doc_content.append("  • xs:integer : Nombre entier")
        doc_content.append("  • xs:decimal : Nombre décimal")
        doc_content.append("")
        doc_content.append("=" * 80)
        doc_content.append("CONTRAINTES")
        doc_content.append("=" * 80)
        doc_content.append("")
        doc_content.append("Attributs obligatoires (use='required') :")
        doc_content.append("  • spotify_data/@generated_at")
        doc_content.append("  • spotify_data/@total_playlists")
        doc_content.append("  • spotify_data/@total_tracks")
        doc_content.append("  • playlist/@id")
        doc_content.append("  • tracks/@count")
        doc_content.append("  • track/@id")
        doc_content.append("  • duration/@ms")
        doc_content.append("  • album/@id")
        doc_content.append("")
        doc_content.append("Cardinalités :")
        doc_content.append("  • playlists : 1 occurrence exactement")
        doc_content.append("  • playlist : 0 à n occurrences")
        doc_content.append("  • tracks : 1 par playlist")
        doc_content.append("  • track : 0 à n par playlist")
        doc_content.append("")
        doc_content.append("=" * 80)
        doc_content.append("EXEMPLE D'UTILISATION")
        doc_content.append("=" * 80)
        doc_content.append("")
        doc_content.append("Pour valider un fichier XML avec ce schéma XSD :")
        doc_content.append("")
        doc_content.append("  python -c \"from services.xsd_validator import print_validation_report; \\")
        doc_content.append("             print_validation_report('./data/output/spotify_data_export.xml', \\")
        doc_content.append("                                    './data/output/spotify_data.xsd')\"")
        doc_content.append("")
        doc_content.append("=" * 80)

        # Écrire dans le fichier
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(doc_content))

        print(f"✅ Documentation générée : {doc_file}")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la génération de la documentation : {e}")
        return False


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module xsd_creator")
    print("=" * 70)

    # Créer le schéma XSD
    xsd_file = "./data/output/spotify_data.xsd"
    success = create_spotify_xsd(xsd_file)

    if success:
        # Générer la documentation
        generate_xsd_documentation(xsd_file)

        print("\n" + "=" * 70)
        print("✅ Schéma XSD et documentation créés avec succès !")
        print("=" * 70)
        print(f"\n📋 Fichiers générés :")
        print(f"   • {xsd_file}")
        print(f"   • ./data/output/XSD_DOCUMENTATION.txt")
    else:
        print("\n❌ Échec de la création du schéma XSD")

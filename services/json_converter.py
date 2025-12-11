
"""
Module de conversion XML vers JSON pour les données Spotify.
Utilise XSLT pour transformer le XML en JSON, puis valide et formate le résultat.
"""

from lxml import etree
from pathlib import Path
import json
import sys


def transform_xml_to_json_via_xslt(xml_file, xslt_file, json_output_file):
    """
    Transforme un fichier XML en JSON via XSLT.

    Args:
        xml_file: Chemin du fichier XML source
        xslt_file: Chemin du fichier XSLT de transformation
        json_output_file: Chemin du fichier JSON de sortie

    Returns:
        tuple: (bool: succès, dict: données JSON ou None)
    """
    print(f"\n🔄 Transformation XML → JSON via XSLT...")
    print(f"📄 Fichier XML   : {xml_file}")
    print(f"📋 Fichier XSLT  : {xslt_file}")
    print(f"💾 Fichier JSON  : {json_output_file}")

    try:
        # 1. Charger le fichier XML
        print("\n📖 Chargement du XML...")
        xml_tree = etree.parse(xml_file)

        # 2. Charger le fichier XSLT
        print("📖 Chargement du XSLT...")
        xslt_tree = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_tree)

        # 3. Appliquer la transformation
        print("⚙️  Transformation en cours...")
        result = transform(xml_tree)

        # 4. Extraire le texte JSON
        json_text = str(result)

        # 5. Valider que c'est du JSON valide
        print("✅ Validation du JSON...")
        try:
            json_data = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"❌ Le JSON généré n'est pas valide : {e}")
            print(f"📝 Contenu généré (premiers 500 caractères) :")
            print(json_text[:500])
            return False, None

        # 6. Sauvegarder le JSON formaté
        print("💾 Sauvegarde du JSON...")
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        # 7. Statistiques
        print("\n✅ Transformation réussie !")
        print_json_statistics(json_data, json_output_file)

        return True, json_data

    except etree.XSLTParseError as e:
        print(f"\n❌ Erreur lors du parsing du XSLT : {e}")
        return False, None

    except etree.XMLSyntaxError as e:
        print(f"\n❌ Erreur de syntaxe XML : {e}")
        return False, None

    except FileNotFoundError as e:
        print(f"\n❌ Fichier introuvable : {e}")
        return False, None

    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False, None


def print_json_statistics(json_data, json_file):
    """
    Affiche des statistiques sur le JSON généré.

    Args:
        json_data: Données JSON (dict)
        json_file: Chemin du fichier JSON
    """
    print(f"\n📊 Statistiques du JSON généré :")

    if isinstance(json_data, dict):
        print(f"   • Total playlists    : {json_data.get('total_playlists', 0)}")
        print(f"   • Total tracks       : {json_data.get('total_tracks', 0)}")

        playlists = json_data.get('playlists', [])
        if playlists:
            total_tracks_in_playlists = sum(len(p.get('tracks', [])) for p in playlists)
            print(f"   • Tracks dans JSON   : {total_tracks_in_playlists}")

    # Taille du fichier
    file_size = Path(json_file).stat().st_size
    print(f"   • Taille fichier     : {file_size:,} bytes ({file_size/1024:.2f} KB)")


def validate_json_structure(json_data):
    """
    Valide que le JSON a la structure attendue pour MongoDB.

    Args:
        json_data: Données JSON à valider

    Returns:
        tuple: (bool: valide, list: erreurs)
    """
    print(f"\n🔍 Validation de la structure JSON...")

    errors = []

    # Vérifier que c'est un dictionnaire
    if not isinstance(json_data, dict):
        errors.append("Le JSON racine doit être un objet (dict)")
        return False, errors

    # Vérifier les champs obligatoires au niveau racine
    required_root_fields = ['generated_at', 'total_playlists', 'total_tracks', 'playlists']
    for field in required_root_fields:
        if field not in json_data:
            errors.append(f"Champ obligatoire manquant : {field}")

    # Vérifier que playlists est une liste
    if 'playlists' in json_data and not isinstance(json_data['playlists'], list):
        errors.append("Le champ 'playlists' doit être une liste")

    # Vérifier la structure de chaque playlist
    if 'playlists' in json_data and isinstance(json_data['playlists'], list):
        for i, playlist in enumerate(json_data['playlists']):
            if not isinstance(playlist, dict):
                errors.append(f"Playlist {i} n'est pas un objet")
                continue

            # Champs obligatoires d'une playlist
            required_playlist_fields = ['id', 'nom', 'genre', 'subgenre', 'tracks']
            for field in required_playlist_fields:
                if field not in playlist:
                    errors.append(f"Playlist {i} : champ obligatoire manquant '{field}'")

            # Vérifier que tracks est une liste
            if 'tracks' in playlist and not isinstance(playlist['tracks'], list):
                errors.append(f"Playlist {i} : 'tracks' doit être une liste")

    if errors:
        print(f"❌ Validation échouée : {len(errors)} erreur(s)")
        for error in errors:
            print(f"   • {error}")
        return False, errors
    else:
        print("✅ Structure JSON valide !")
        return True, []


def convert_xml_to_json(xml_file, xslt_file, json_output_file):
    """
    Pipeline complet : XML → JSON via XSLT avec validation.

    Args:
        xml_file: Chemin du fichier XML
        xslt_file: Chemin du fichier XSLT
        json_output_file: Chemin du fichier JSON de sortie

    Returns:
        tuple: (bool: succès, dict: données JSON ou None)
    """
    print("\n" + "="*70)
    print(" 🔄 CONVERSION XML → JSON")
    print("="*70)

    # Étape 1 : Transformation XSLT
    success, json_data = transform_xml_to_json_via_xslt(xml_file, xslt_file, json_output_file)

    if not success:
        print("\n❌ Échec de la transformation")
        return False, None

    # Étape 2 : Validation de la structure
    valid, errors = validate_json_structure(json_data)

    if not valid:
        print("\n⚠️  Le JSON est valide syntaxiquement mais la structure est incorrecte")
        return False, None

    print("\n" + "="*70)
    print(" ✅ CONVERSION RÉUSSIE")
    print("="*70)

    return True, json_data


def pretty_print_json_sample(json_file, num_playlists=2):
    """
    Affiche un échantillon du JSON de manière formatée.

    Args:
        json_file: Chemin du fichier JSON
        num_playlists: Nombre de playlists à afficher
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n📋 Aperçu du JSON (premières {num_playlists} playlists) :")
        print("-" * 70)

        sample = {
            'generated_at': data.get('generated_at'),
            'total_playlists': data.get('total_playlists'),
            'total_tracks': data.get('total_tracks'),
            'playlists': data.get('playlists', [])[:num_playlists]
        }

        print(json.dumps(sample, indent=2, ensure_ascii=False))
        print("-" * 70)

    except Exception as e:
        print(f"❌ Erreur lors de l'affichage : {e}")


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module json_converter")
    print("="*70)

    # Chemins de test
    xml_file = "./data/output/spotify_data_export.xml"
    xslt_file = "./data/input/spotify_to_json.xslt"
    json_file = "./data/output/spotify_data.json"

    # Vérifier que les fichiers existent
    if not Path(xml_file).exists():
        print(f"⚠️  Fichier XML de test non trouvé : {xml_file}")
        print("💡 Exécute d'abord : python main.py --full-reset")
        sys.exit(1)

    if not Path(xslt_file).exists():
        print(f"⚠️  Fichier XSLT de test non trouvé : {xslt_file}")
        print("💡 Le fichier XSLT doit être créé")
        sys.exit(1)

    # Conversion complète
    success, json_data = convert_xml_to_json(xml_file, xslt_file, json_file)

    if success:
        # Afficher un échantillon
        pretty_print_json_sample(json_file, num_playlists=2)

        print(f"\n✅ Fichier JSON créé : {json_file}")
    else:
        print("\n❌ Échec de la conversion")
        sys.exit(1)

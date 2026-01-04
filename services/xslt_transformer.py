"""
Module de transformation XSLT pour convertir le XML Spotify en HTML.
Utilise lxml pour appliquer une feuille de style XSLT.
"""

from lxml import etree
from pathlib import Path
from datetime import datetime

# Import de la configuration
try:
    from configs.config import XSLT_FILE_PATH, HTML_OUTPUT_PATH
except ImportError:
    # Valeurs par défaut si la config n'existe pas
    XSLT_FILE_PATH = "./data/input/spotify_transform.xslt"
    HTML_OUTPUT_PATH = "./data/output/spotify_data.html"


def transform_to_html(xml_file, xslt_file=None, output_file=None):
    """
    Transforme un fichier XML en HTML en utilisant XSLT.

    Args:
        xml_file: Chemin du fichier XML source
        xslt_file: Chemin du fichier XSLT (optionnel, utilise la config par défaut)
        output_file: Chemin du fichier HTML de sortie (optionnel)

    Returns:
        str: Chemin du fichier HTML généré, ou None en cas d'erreur
    """

    # Utiliser les valeurs par défaut si non spécifiées
    if xslt_file is None:
        xslt_file = XSLT_FILE_PATH

    if output_file is None:
        output_file = HTML_OUTPUT_PATH

    print(f"\n🔄 Transformation XSLT → HTML...")
    print(f" Fichier XML   : {xml_file}")
    print(f" Fichier XSLT  : {xslt_file}")
    print(f" Fichier HTML  : {output_file}")

    try:
        # Vérifier l'existence des fichiers d'entrée
        xml_path = Path(xml_file)
        xslt_path = Path(xslt_file)

        if not xml_path.exists():
            print(f"❌ Fichier XML introuvable : {xml_file}")
            return None

        if not xslt_path.exists():
            print(f"❌ Fichier XSLT introuvable : {xslt_file}")
            return None

        # Créer le répertoire de sortie s'il n'existe pas
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Charger le document XML
        print("\n📖 Chargement du document XML...")
        xml_doc = etree.parse(str(xml_path))

        # Charger la feuille de style XSLT
        print("📖 Chargement de la feuille de style XSLT...")
        xslt_doc = etree.parse(str(xslt_path))

        # Créer le transformateur XSLT
        print("⚙️  Création du transformateur XSLT...")
        transform = etree.XSLT(xslt_doc)

        # Appliquer la transformation
        print("🔄 Application de la transformation...")
        result_tree = transform(xml_doc)

        # Vérifier les erreurs de transformation
        if transform.error_log:
            print("\n⚠️  Avertissements lors de la transformation :")
            for error in transform.error_log:
                print(f"   • {error.message}")

        # Écrire le résultat dans le fichier HTML
        print(f"💾 Écriture du fichier HTML...")
        with open(output_path, 'wb') as f:
            f.write(etree.tostring(
                result_tree,
                pretty_print=True,
                method='html',
                encoding='UTF-8'
            ))

        # Calculer la taille du fichier
        file_size = output_path.stat().st_size
        file_size_kb = file_size / 1024

        # Statistiques du document XML
        root = xml_doc.getroot()
        total_playlists = root.get('total_playlists', '0')
        total_tracks = root.get('total_tracks', '0')

        print(f"\n Transformation réussie !")
        print(f" Fichier généré : {output_file}")
        print(f" Taille        : {file_size_kb:.2f} KB")
        print(f" Contenu       : {total_playlists} playlists, {total_tracks} tracks")
        print(f"\n Ouvrez le fichier dans un navigateur pour visualiser les données.")

        return str(output_path)

    except etree.XSLTParseError as e:
        print(f"\n❌ Erreur de parsing XSLT : {e}")
        print(f"   Vérifiez la syntaxe du fichier XSLT : {xslt_file}")
        return None

    except etree.XMLSyntaxError as e:
        print(f"\n❌ Erreur de syntaxe XML : {e}")
        print(f"   Vérifiez la validité du fichier XML : {xml_file}")
        return None

    except Exception as e:
        print(f"\n❌ Erreur lors de la transformation : {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_xslt(xslt_file=None):
    """
    Valide qu'un fichier XSLT est bien formé et syntaxiquement correct.

    Args:
        xslt_file: Chemin du fichier XSLT (optionnel)

    Returns:
        bool: True si le XSLT est valide, False sinon
    """
    if xslt_file is None:
        xslt_file = XSLT_FILE_PATH

    print(f"\n🔍 Validation du fichier XSLT...")
    print(f" Fichier : {xslt_file}")

    try:
        xslt_path = Path(xslt_file)

        if not xslt_path.exists():
            print(f"❌ Fichier introuvable : {xslt_file}")
            return False

        # Tenter de parser le document XSLT
        xslt_doc = etree.parse(str(xslt_path))

        # Tenter de créer un transformateur (validation complète)
        transform = etree.XSLT(xslt_doc)

        print(" Le fichier XSLT est valide.")
        return True

    except etree.XSLTParseError as e:
        print(f"❌ Erreur de parsing XSLT : {e}")
        return False

    except etree.XMLSyntaxError as e:
        print(f"❌ Erreur de syntaxe XML dans le XSLT : {e}")
        return False

    except Exception as e:
        print(f"❌ Erreur lors de la validation : {e}")
        return False


def get_xslt_info(xslt_file=None):
    """
    Affiche des informations sur le fichier XSLT.

    Args:
        xslt_file: Chemin du fichier XSLT (optionnel)
    """
    if xslt_file is None:
        xslt_file = XSLT_FILE_PATH

    try:
        xslt_path = Path(xslt_file)

        if not xslt_path.exists():
            print(f"❌ Fichier introuvable : {xslt_file}")
            return

        # Lire le fichier XSLT
        xslt_doc = etree.parse(str(xslt_path))
        root = xslt_doc.getroot()

        # Informations du fichier
        file_size = xslt_path.stat().st_size
        file_size_kb = file_size / 1024

        print(f"\n Informations XSLT")
        print("=" * 60)
        print(f" Fichier       : {xslt_file}")
        print(f" Taille        : {file_size_kb:.2f} KB")
        print(f"🔖 Version XSLT  : {root.get('version', 'Non spécifié')}")

        # Compter les templates
        templates = root.xpath('//xsl:template', namespaces={'xsl': 'http://www.w3.org/1999/XSL/Transform'})
        print(f"📝 Templates     : {len(templates)}")

        print("=" * 60)

    except Exception as e:
        print(f"❌ Erreur lors de la lecture des informations : {e}")


# Point d'entrée pour test direct
if __name__ == '__main__':
    import sys

    print("=" * 70)
    print("XSLT TRANSFORMER - MODULE DE TRANSFORMATION XML > HTML".center(70))
    print("=" * 70)

    # Si un fichier XML est passé en argument
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
        xslt_file = sys.argv[2] if len(sys.argv) > 2 else None
        output_file = sys.argv[3] if len(sys.argv) > 3 else None

        result = transform_to_html(xml_file, xslt_file, output_file)

        if result:
            print(f"\n🎉 Transformation terminée avec succès !")
            sys.exit(0)
        else:
            print(f"\n💥 La transformation a échoué.")
            sys.exit(1)
    else:
        # Mode information
        print("\n📖 Usage :")
        print("   python xslt_transformer.py <fichier_xml> [fichier_xslt] [fichier_html]")
        print("\nExemple :")
        print("   python xslt_transformer.py data/output/spotify_data_export.xml")
        print()

        # Afficher les informations XSLT par défaut
        get_xslt_info()

        # Valider le XSLT par défaut
        validate_xslt()

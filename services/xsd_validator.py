
"""
Module de validation XSD pour les données Spotify.
Valide un fichier XML contre un schéma XSD (XML Schema Definition).
"""

from lxml import etree
from pathlib import Path
import sys


def validate_xml_with_xsd(xml_file, xsd_file):
    """
    Valide un fichier XML contre un schéma XSD.

    Args:
        xml_file: Chemin du fichier XML à valider
        xsd_file: Chemin du fichier XSD

    Returns:
        tuple: (bool: succès, list: liste des erreurs)
    """
    print(f"\n🔍 Validation du XML avec le schéma XSD...")
    print(f"📄 Fichier XML : {xml_file}")
    print(f" Fichier XSD : {xsd_file}")

    try:
        # Charger le schéma XSD
        with open(xsd_file, 'rb') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)

        # Parser le XML
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)

        # Valider
        is_valid = schema.validate(tree)

        if is_valid:
            print("\n Le fichier XML est VALIDE selon le schéma XSD !")
            print(" Toutes les règles de structure et de typage sont respectées.")
            return True, []
        else:
            print("\n Le fichier XML est INVALIDE !")
            print(" Erreurs de validation :")

            errors = []
            for error in schema.error_log:
                error_msg = f"  • Ligne {error.line} : {error.message}"
                print(error_msg)
                errors.append({
                    'line': error.line,
                    'message': error.message,
                    'type': error.type_name,
                    'domain': error.domain_name
                })

            return False, errors

    except etree.XMLSchemaParseError as e:
        print(f"\n Erreur lors du parsing du schéma XSD : {e}")
        return False, [{'line': 0, 'message': str(e), 'type': 'XSD_PARSE_ERROR'}]

    except etree.XMLSyntaxError as e:
        print(f"\n Erreur de syntaxe XML : {e}")
        return False, [{'line': e.lineno, 'message': str(e), 'type': 'XML_SYNTAX_ERROR'}]

    except FileNotFoundError as e:
        print(f"\n Fichier introuvable : {e}")
        return False, [{'line': 0, 'message': str(e), 'type': 'FILE_NOT_FOUND'}]

    except Exception as e:
        print(f"\n Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False, [{'line': 0, 'message': str(e), 'type': 'UNKNOWN_ERROR'}]


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module xsd_validator")
    print("="*70)

    # Chemins de test
    xml_file = "./data/output/spotify_data_export.xml"
    xsd_file = "./data/output/spotify_data.xsd"

    # Vérifier que les fichiers existent
    if not Path(xml_file).exists():
        print(f"⚠️  Fichier XML de test non trouvé : {xml_file}")
        print("💡 Exécute d'abord : python main.py --full-reset")
        sys.exit(1)

    if not Path(xsd_file).exists():
        print(f"⚠️  Fichier XSD de test non trouvé : {xsd_file}")
        print("💡 Le schéma XSD sera généré automatiquement.")
        sys.exit(1)


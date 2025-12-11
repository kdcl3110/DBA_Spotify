
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
    print(f"📋 Fichier XSD : {xsd_file}")

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
            print("\n✅ Le fichier XML est VALIDE selon le schéma XSD !")
            print("📋 Toutes les règles de structure et de typage sont respectées.")
            return True, []
        else:
            print("\n❌ Le fichier XML est INVALIDE !")
            print("📋 Erreurs de validation :")

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
        print(f"\n❌ Erreur lors du parsing du schéma XSD : {e}")
        return False, [{'line': 0, 'message': str(e), 'type': 'XSD_PARSE_ERROR'}]

    except etree.XMLSyntaxError as e:
        print(f"\n❌ Erreur de syntaxe XML : {e}")
        return False, [{'line': e.lineno, 'message': str(e), 'type': 'XML_SYNTAX_ERROR'}]

    except FileNotFoundError as e:
        print(f"\n❌ Fichier introuvable : {e}")
        return False, [{'line': 0, 'message': str(e), 'type': 'FILE_NOT_FOUND'}]

    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        return False, [{'line': 0, 'message': str(e), 'type': 'UNKNOWN_ERROR'}]


def validate_xml_well_formed(xml_file):
    """
    Vérifie que le XML est bien formé (syntaxe correcte).

    Args:
        xml_file: Chemin du fichier XML

    Returns:
        tuple: (bool: succès, str: message)
    """
    print(f"\n🔍 Vérification de la syntaxe XML...")
    print(f"📄 Fichier : {xml_file}")

    try:
        etree.parse(xml_file)
        print("✅ Le fichier XML est bien formé (syntaxe correcte).")
        return True, "XML bien formé"

    except etree.XMLSyntaxError as e:
        print(f"❌ Erreur de syntaxe XML : {e}")
        return False, str(e)

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False, str(e)


def get_xml_statistics(xml_file):
    """
    Extrait des statistiques du fichier XML.

    Args:
        xml_file: Chemin du fichier XML

    Returns:
        dict: Statistiques du XML
    """
    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()

        stats = {
            'root_tag': root.tag,
            'total_elements': len(list(root.iter())),
            'playlists': len(root.findall('.//playlist')),
            'tracks': len(root.findall('.//track')),
            'albums': len(root.findall('.//album')),
            'artists': len(root.findall('.//artist')),
            'audio_features': len(root.findall('.//audio_features')),
            'file_size': Path(xml_file).stat().st_size
        }

        return stats

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction des statistiques : {e}")
        return None


def print_validation_report(xml_file, xsd_file):
    """
    Génère un rapport de validation complet.

    Args:
        xml_file: Chemin du fichier XML
        xsd_file: Chemin du fichier XSD
    """
    print("\n" + "="*70)
    print(" 📊 RAPPORT DE VALIDATION XML/XSD")
    print("="*70)

    # 1. Vérifier que les fichiers existent
    xml_path = Path(xml_file)
    xsd_path = Path(xsd_file)

    if not xml_path.exists():
        print(f"\n❌ Fichier XML introuvable : {xml_file}")
        return

    if not xsd_path.exists():
        print(f"\n❌ Fichier XSD introuvable : {xsd_file}")
        return

    print(f"\n📄 Fichier XML : {xml_file}")
    print(f"📋 Fichier XSD : {xsd_file}")

    # 2. Statistiques des fichiers
    xml_size = xml_path.stat().st_size / 1024
    xsd_size = xsd_path.stat().st_size / 1024

    print(f"\n📊 Taille des fichiers :")
    print(f"   • XML : {xml_size:.2f} KB")
    print(f"   • XSD : {xsd_size:.2f} KB")

    # 3. Vérifier syntaxe XML
    print("\n" + "-"*70)
    print(" ÉTAPE 1 : Vérification syntaxe XML")
    print("-"*70)

    well_formed, msg = validate_xml_well_formed(xml_file)

    if not well_formed:
        print("\n⚠️  Le XML n'est pas bien formé. Validation XSD impossible.")
        return

    # 4. Statistiques du contenu
    print("\n" + "-"*70)
    print(" ÉTAPE 2 : Statistiques du contenu")
    print("-"*70)

    stats = get_xml_statistics(xml_file)

    if stats:
        print(f"\n📊 Contenu du XML :")
        print(f"   • Élément racine    : {stats['root_tag']}")
        print(f"   • Total éléments    : {stats['total_elements']}")
        print(f"   • Playlists         : {stats['playlists']}")
        print(f"   • Tracks            : {stats['tracks']}")
        print(f"   • Albums            : {stats['albums']}")
        print(f"   • Artistes          : {stats['artists']}")
        print(f"   • Audio features    : {stats['audio_features']}")

    # 5. Validation XSD
    print("\n" + "-"*70)
    print(" ÉTAPE 3 : Validation avec XSD")
    print("-"*70)

    is_valid, errors = validate_xml_with_xsd(xml_file, xsd_file)

    # 6. Résumé final
    print("\n" + "="*70)
    print(" 📋 RÉSUMÉ")
    print("="*70)

    if well_formed and is_valid:
        print("\n✅ VALIDATION RÉUSSIE")
        print("   • Le XML est bien formé")
        print("   • Le XML est conforme au schéma XSD")
        print("   • Aucune erreur détectée")
    elif well_formed and not is_valid:
        print("\n⚠️  VALIDATION PARTIELLE")
        print("   • Le XML est bien formé")
        print("   • Le XML n'est PAS conforme au schéma XSD")
        print(f"   • {len(errors)} erreur(s) détectée(s)")
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("   • Le XML n'est pas bien formé")
        print("   • Impossible de valider avec le schéma XSD")

    print("\n" + "="*70)


def get_xsd_info(xsd_file):
    """
    Extrait des informations du schéma XSD.

    Args:
        xsd_file: Chemin du fichier XSD

    Returns:
        dict: Informations du schéma
    """
    try:
        tree = etree.parse(xsd_file)
        root = tree.getroot()

        # Namespace XSD
        ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}

        info = {
            'elements': len(root.findall('.//xs:element', ns)),
            'complex_types': len(root.findall('.//xs:complexType', ns)),
            'simple_types': len(root.findall('.//xs:simpleType', ns)),
            'attributes': len(root.findall('.//xs:attribute', ns)),
            'target_namespace': root.get('targetNamespace', 'None')
        }

        print(f"\n📋 Informations du schéma XSD :")
        print(f"   • Éléments définis    : {info['elements']}")
        print(f"   • Types complexes     : {info['complex_types']}")
        print(f"   • Types simples       : {info['simple_types']}")
        print(f"   • Attributs           : {info['attributes']}")
        print(f"   • Namespace cible     : {info['target_namespace']}")

        return info

    except Exception as e:
        print(f"❌ Erreur lors de l'extraction des informations XSD : {e}")
        return None


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

    # Informations sur le schéma
    get_xsd_info(xsd_file)

    # Rapport complet
    print_validation_report(xml_file, xsd_file)

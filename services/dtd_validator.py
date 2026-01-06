
"""
Module de validation DTD pour les données Spotify.
Valide un fichier XML contre une DTD (Document Type Definition).
"""

from lxml import etree
from pathlib import Path
import sys


def validate_xml_with_dtd(xml_file, dtd_file):
    """
    Valide un fichier XML contre une DTD.
    
    Args:
        xml_file: Chemin du fichier XML à valider
        dtd_file: Chemin du fichier DTD
        
    Returns:
        tuple: (bool: succès, list: liste des erreurs)
    """
    print(f"\n🔍 Validation du XML avec la DTD...")
    print(f"📄 Fichier XML : {xml_file}")
    print(f"📋 Fichier DTD : {dtd_file}")
    
    try:
        # Charger la DTD
        with open(dtd_file, 'rb') as f:
            dtd = etree.DTD(f)
        
        # Parser le XML
        parser = etree.XMLParser(dtd_validation=False)
        tree = etree.parse(xml_file, parser)
        
        # Valider
        is_valid = dtd.validate(tree)
        
        if is_valid:
            print("\n✅ Le fichier XML est VALIDE selon la DTD !")
            print("📋 Toutes les règles de structure sont respectées.")
            return True, []
        else:
            print("\n❌ Le fichier XML est INVALIDE !")
            print("📋 Erreurs de validation :")
            
            errors = []
            for error in dtd.error_log:
                error_msg = f"  • Ligne {error.line} : {error.message}"
                print(error_msg)
                errors.append({
                    'line': error.line,
                    'message': error.message,
                    'type': error.type_name
                })
            
            return False, errors
    
    except etree.DTDParseError as e:
        print(f"\n❌ Erreur lors du parsing de la DTD : {e}")
        return False, [{'line': 0, 'message': str(e), 'type': 'DTD_PARSE_ERROR'}]
    
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



# Test du module
if __name__ == "__main__":
    print("🧪 Test du module dtd_validator")
    print("="*70)
    
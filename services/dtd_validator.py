
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


def print_validation_report(xml_file, dtd_file):
    """
    Génère un rapport de validation complet.
    
    Args:
        xml_file: Chemin du fichier XML
        dtd_file: Chemin du fichier DTD
    """
    print("\n" + "="*70)
    print(" 📊 RAPPORT DE VALIDATION XML/DTD")
    print("="*70)
    
    # 1. Vérifier que les fichiers existent
    xml_path = Path(xml_file)
    dtd_path = Path(dtd_file)
    
    if not xml_path.exists():
        print(f"\n❌ Fichier XML introuvable : {xml_file}")
        return
    
    if not dtd_path.exists():
        print(f"\n❌ Fichier DTD introuvable : {dtd_file}")
        return
    
    print(f"\n📄 Fichier XML : {xml_file}")
    print(f"📋 Fichier DTD : {dtd_file}")
    
    # 2. Statistiques des fichiers
    xml_size = xml_path.stat().st_size / 1024
    dtd_size = dtd_path.stat().st_size / 1024
    
    print(f"\n📊 Taille des fichiers :")
    print(f"   • XML : {xml_size:.2f} KB")
    print(f"   • DTD : {dtd_size:.2f} KB")
    
    # 3. Vérifier syntaxe XML
    print("\n" + "-"*70)
    print(" ÉTAPE 1 : Vérification syntaxe XML")
    print("-"*70)
    
    well_formed, msg = validate_xml_well_formed(xml_file)
    
    if not well_formed:
        print("\n⚠️  Le XML n'est pas bien formé. Validation DTD impossible.")
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
    
    # 5. Validation DTD
    print("\n" + "-"*70)
    print(" ÉTAPE 3 : Validation avec DTD")
    print("-"*70)
    
    is_valid, errors = validate_xml_with_dtd(xml_file, dtd_file)
    
    # 6. Résumé final
    print("\n" + "="*70)
    print(" 📋 RÉSUMÉ")
    print("="*70)
    
    if well_formed and is_valid:
        print("\n✅ VALIDATION RÉUSSIE")
        print("   • Le XML est bien formé")
        print("   • Le XML est conforme à la DTD")
        print("   • Aucune erreur détectée")
    elif well_formed and not is_valid:
        print("\n⚠️  VALIDATION PARTIELLE")
        print("   • Le XML est bien formé")
        print("   • Le XML n'est PAS conforme à la DTD")
        print(f"   • {len(errors)} erreur(s) détectée(s)")
    else:
        print("\n❌ VALIDATION ÉCHOUÉE")
        print("   • Le XML n'est pas bien formé")
        print("   • Impossible de valider avec la DTD")
    
    print("\n" + "="*70)


def fix_common_xml_issues(xml_file):
    """
    Tente de corriger les problèmes courants dans le XML.
    
    Args:
        xml_file: Chemin du fichier XML
        
    Returns:
        bool: True si des corrections ont été apportées
    """
    print(f"\n🔧 Tentative de correction automatique...")
    print(f"📄 Fichier : {xml_file}")
    
    try:
        # Lire le contenu
        with open(xml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        corrections = []
        
        # Correction 1 : Vérifier l'encodage
        if not content.startswith('<?xml'):
            content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
            corrections.append("Ajout de la déclaration XML")
        
        # Correction 2 : Enlever les espaces dans les balises
        import re
        if re.search(r'<\s+\w+|<\w+\s+>', content):
            content = re.sub(r'<\s+(\w+)', r'<\1', content)
            content = re.sub(r'<(\w+)\s+>', r'<\1>', content)
            corrections.append("Suppression des espaces dans les balises")
        
        # Si des corrections ont été faites
        if content != original_content:
            # Sauvegarder une backup
            backup_file = str(xml_file) + '.backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Sauvegarder le fichier corrigé
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {len(corrections)} correction(s) appliquée(s) :")
            for correction in corrections:
                print(f"   • {correction}")
            print(f"💾 Backup sauvegardé : {backup_file}")
            
            return True
        else:
            print("ℹ️  Aucune correction nécessaire.")
            return False
    
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        return False


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module dtd_validator")
    print("="*70)
    
    # Chemins de test
    xml_file = "./data/output/spotify_data_export.xml"
    dtd_file = "./data/output/spotify_data.dtd"
    
    # Vérifier que les fichiers existent
    if not Path(xml_file).exists():
        print(f"⚠️  Fichier XML de test non trouvé : {xml_file}")
        print("💡 Exécute d'abord : python main.py --full-reset")
        sys.exit(1)
    
    if not Path(dtd_file).exists():
        print(f"⚠️  Fichier DTD de test non trouvé : {dtd_file}")
        print("💡 Exécute d'abord : python services/dtd_creator.py")
        sys.exit(1)
    
    # Rapport complet
    print_validation_report(xml_file, dtd_file)
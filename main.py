# Fichier : main.py

"""
Point d'entrée principal pour le pipeline de données Spotify.

Pipeline complet :
1. Extraction et normalisation des données CSV
2. Initialisation de la base de données Oracle
3. Insertion des données normalisées
4. Export des données vers XML
5. Validation DTD
6. Transformation XSLT vers HTML
"""

import sys
import argparse
from pathlib import Path

# Imports des modules du projet
from DB.db_manager import DatabaseManager
from services.data_processor import preprocess_csv
from services.xml_exporter import export_to_xml, validate_xml_structure
from services.dtd_validator import validate_xml_with_dtd
from services.dtd_creator import create_spotify_dtd, print_dtd_info, generate_dtd_documentation
from services.xslt_transformer import transform_to_html


def print_banner(text, char="="):
    """Affiche un bandeau décoratif."""
    width = 70
    print("\n" + char * width)
    print(f"{text.center(width)}")
    print(char * width + "\n")


def run_ingestion_process(initialize=False, drop_first=False):
    """
    Orchestre le processus complet de lecture CSV, initialisation BD et insertion.
    
    Args:
        initialize: Si True, initialise/crée les tables de la BD
        drop_first: Si True, supprime d'abord les tables existantes
        
    Returns:
        bool: True si le processus s'est terminé avec succès
    """
    
    print_banner("🎵 PIPELINE D'INGESTION SPOTIFY 🎵")
    
    # ==============================================
    # ÉTAPE 1 : PRÉTRAITEMENT DES DONNÉES CSV
    # ==============================================
    print_banner("ÉTAPE 1 : EXTRACTION ET NORMALISATION CSV", "-")
    
    try:
        data_to_insert = preprocess_csv()
        
        # Vérifier que le dictionnaire contient des DataFrames valides
        if not data_to_insert or 'sp_genres' not in data_to_insert:
            print("❌ Erreur : Aucune donnée n'a été extraite du CSV.")
            return False
        
        # Vérifier que les DataFrames ne sont pas vides
        if data_to_insert['sp_genres'].empty:
            print("❌ Erreur : Les données extraites sont vides.")
            return False
        
        print("✅ Données CSV extraites et normalisées avec succès.\n")
        
    except FileNotFoundError as e:
        print(f"❌ Fichier CSV introuvable : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du prétraitement CSV : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # ==============================================
    # ÉTAPE 2 : CONNEXION À LA BASE DE DONNÉES
    # ==============================================
    print_banner("ÉTAPE 2 : CONNEXION À ORACLE", "-")
    
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("❌ Impossible de se connecter à la base de données.")
        return False
    
    try:
        # ==============================================
        # ÉTAPE 3 : INITIALISATION DE LA BASE DE DONNÉES
        # ==============================================
        if initialize:
            print_banner("ÉTAPE 3 : INITIALISATION DES TABLES", "-")
            
            if drop_first:
                print("⚠️  Mode RESET activé : les tables existantes seront supprimées.\n")
            
            success = db_manager.initialize_db(drop_first=drop_first)
            
            if not success:
                print("⚠️  Initialisation terminée avec des avertissements.")
            else:
                print("✅ Base de données initialisée avec succès.\n")
        else:
            print("ℹ️  Initialisation de la BD ignorée (initialize=False).\n")
        
        # ==============================================
        # ÉTAPE 4 : INSERTION DES DONNÉES
        # ==============================================
        print_banner("ÉTAPE 4 : INSERTION DES DONNÉES", "-")
        
        success = db_manager.insert_data(data_to_insert)
        
        if not success:
            print("❌ Erreur lors de l'insertion des données.")
            return False
        
        print("✅ Toutes les données ont été insérées avec succès.\n")
        
        # ==============================================
        # ÉTAPE 5 : VÉRIFICATION DES STATISTIQUES
        # ==============================================
        print_banner("ÉTAPE 5 : STATISTIQUES DE LA BASE", "-")
        
        stats = db_manager.get_statistics()
        
        if stats:
            print("📊 Nombre d'enregistrements par table :")
            print("-" * 50)
            for table, count in stats.items():
                table_name = table.replace('sp_', '').upper()
                print(f"  • {table_name:<25} : {count:>6} lignes")
            print("-" * 50 + "\n")
        
        # ==============================================
        # ÉTAPE 6 : EXTRACTION POUR XML (PRÉPARATION)
        # ==============================================
        print_banner("ÉTAPE 6 : EXTRACTION POUR XML", "-")
        
        xml_data = db_manager.fetch_data_for_xml()
        
        if not xml_data:
            print("⚠️  Aucune donnée à exporter vers XML.")
        else:
            print(f"✅ {len(xml_data)} enregistrements prêts pour l'export XML.\n")
            
            # ==============================================
            # ÉTAPES SUIVANTES DU PIPELINE
            # ==============================================
            print_banner("ÉTAPES SUIVANTES DU PIPELINE", "-")
            print("📝 Pipeline complet :")
            print("  1. ✅ Extraction CSV")
            print("  2. ✅ Insertion Oracle")
            print("  3. ✅ Génération XML")
            print("  4. ✅ Création DTD")
            print("  5. ✅ Validation DTD")
            print("  6. ⏳ Transformation XSLT → HTML")
            print()
            
            # Décommenter quand les modules seront créés :
            print("🔄 Génération du fichier XML...")
            xml_file = export_to_xml(xml_data)

            # Générer la DTD avant tout
            dtd_file = create_spotify_dtd()
            
            if dtd_file:
                print("\n✅Création DTD réussie !")
                # Générer la documentation
                generate_dtd_documentation()

                print("🔄 Validation avec DTD...")
                is_valid = validate_xml_with_dtd(xml_file, dtd_file)
                if is_valid:
                    print("\n" + "=" * 70)
                    print("ÉTAPE 7 : TRANSFORMATION XSLT → HTML".center(70))
                    print("=" * 70)
                    html_file = transform_to_html(xml_file)
                    if html_file:
                        print(f"\n✅ Fichier HTML généré : {html_file}")
                    else:
                        print("\n⚠️  La transformation HTML a échoué.")
            else:
                print("\n❌ Test échoué.")

        print_banner("✅ PROCESSUS TERMINÉ AVEC SUCCÈS ✅")
        return True
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Processus interrompu par l'utilisateur.")
        return False
    
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Fermeture de la connexion dans tous les cas
        db_manager.close()


def run_xml_export_only():
    """
    Exporte uniquement les données existantes de la BD vers XML.
    Utile si les données sont déjà en base.
    """
    print_banner("🎵 EXPORT XML DEPUIS LA BASE 🎵")
    
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("❌ Impossible de se connecter à la base de données.")
        return False
    
    try:
        xml_data = db_manager.fetch_data_for_xml()
        
        if not xml_data:
            print("❌ Aucune donnée trouvée en base.")
            return False
        
        print(f"✅ {len(xml_data)} enregistrements prêts pour l'export XML.\n")
        print_banner("ÉTAPE 7 : EXPORT VERS XML", "-")
        
        xml_file = export_to_xml(xml_data)
        
        if xml_file:
            print(f"\n✅ Export XML terminé avec succès !")
            
            # Validation du XML
            validate_xml_structure(xml_file)
        else:
            print("\n⚠️  L'export XML a échoué.")
    
        return True
    except ImportError as e:
            print(f"\n⚠️  Module xml_exporter non trouvé : {e}")
            print("💡 Assurez-vous que services/xml_exporter.py existe")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db_manager.close()


def test_connection():
    """Teste uniquement la connexion à la base de données."""
    print_banner("🔌 TEST DE CONNEXION ORACLE 🔌")
    
    db_manager = DatabaseManager()
    
    if db_manager.connect():
        print("✅ Connexion réussie !")
        
        # Test de requête simple
        try:
            stats = db_manager.get_statistics()
            if stats:
                print("\n📊 Tables détectées :")
                for table, count in stats.items():
                    print(f"  • {table} : {count} lignes")
            else:
                print("\nℹ️  Aucune table détectée (base vide ou non initialisée).")
        except:
            print("\nℹ️  Impossible de récupérer les statistiques (tables non créées).")
        
        db_manager.close()
        return True
    else:
        print("❌ Échec de la connexion.")
        return False


def main():
    """
    Fonction principale avec gestion des arguments en ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Pipeline de données Spotify : CSV → Oracle → XML → HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :
  
  # Ingestion complète (drop + create + insert)
  python main.py --full-reset
  
  # Ingestion sans suppression des tables
  python main.py --initialize
  
  # Insertion seule (tables déjà créées)
  python main.py
  
  # Export XML uniquement
  python main.py --export-xml
  
  # Test de connexion
  python main.py --test-connection
        """
    )
    
    parser.add_argument(
        '--full-reset',
        action='store_true',
        help='Supprime et recrée toutes les tables avant insertion'
    )
    
    parser.add_argument(
        '--initialize',
        action='store_true',
        help='Crée les tables si elles n\'existent pas (sans suppression)'
    )
    
    parser.add_argument(
        '--export-xml',
        action='store_true',
        help='Exporte uniquement les données vers XML (sans insertion)'
    )
    
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Teste uniquement la connexion à Oracle'
    )
    
    args = parser.parse_args()
    
    # Traitement des arguments
    if args.test_connection:
        success = test_connection()
    elif args.export_xml:
        success = run_xml_export_only()
    elif args.full_reset:
        success = run_ingestion_process(initialize=True, drop_first=True)
    elif args.initialize:
        success = run_ingestion_process(initialize=True, drop_first=False)
    else:
        # Mode par défaut : insertion seule (tables déjà créées)
        success = run_ingestion_process(initialize=False, drop_first=False)
    
    # Code de sortie
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
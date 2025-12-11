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
from DB.mongodb_manager import MongoDBManager
from services.data_processor import preprocess_csv
from services.xml_exporter import export_to_xml, validate_xml_structure
from services.dtd_validator import validate_xml_with_dtd
from services.dtd_creator import create_spotify_dtd, generate_dtd_documentation
from services.xslt_transformer import transform_to_html
from services.xsd_validator import validate_xml_with_xsd
from services.xsd_creator import create_spotify_xsd, generate_xsd_documentation
from services.json_converter import convert_xml_to_json

# Imports de configuration
from configs.config import (
    XML_OUTPUT_PATH, XSD_PATH, XSLT_JSON_PATH, JSON_OUTPUT_PATH,
    MONGO_HOST, MONGO_PORT, MONGO_DATABASE
)


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


def run_mongodb_pipeline():
    """
    Exécute le pipeline complet : XML → XSD validation → XSLT → JSON → MongoDB

    Pipeline :
    1. Génération du schéma XSD
    2. Validation du XML avec le XSD
    3. Transformation XSLT : XML → JSON
    4. Insertion du JSON dans MongoDB

    Returns:
        bool: True si le processus s'est terminé avec succès
    """
    print_banner("🍃 PIPELINE XML → XSD → JSON → MONGODB 🍃")

    try:
        # ==============================================
        # ÉTAPE 1 : VÉRIFICATION DU FICHIER XML
        # ==============================================
        print_banner("ÉTAPE 1 : VÉRIFICATION DU FICHIER XML", "-")

        xml_file = Path(XML_OUTPUT_PATH)

        if not xml_file.exists():
            print(f"❌ Fichier XML introuvable : {XML_OUTPUT_PATH}")
            print("💡 Exécutez d'abord : python main.py --full-reset")
            print("   pour générer le fichier XML depuis Oracle")
            return False

        print(f"✅ Fichier XML trouvé : {XML_OUTPUT_PATH}\n")

        # ==============================================
        # ÉTAPE 2 : GÉNÉRATION DU SCHÉMA XSD
        # ==============================================
        print_banner("ÉTAPE 2 : GÉNÉRATION DU SCHÉMA XSD", "-")

        success = create_spotify_xsd(XSD_PATH)

        if not success:
            print("❌ Échec de la génération du schéma XSD")
            return False

        # Générer la documentation XSD
        generate_xsd_documentation(XSD_PATH)

        print("✅ Schéma XSD créé avec succès.\n")

        # ==============================================
        # ÉTAPE 3 : VALIDATION XML AVEC XSD
        # ==============================================
        print_banner("ÉTAPE 3 : VALIDATION XML AVEC XSD", "-")

        is_valid, errors = validate_xml_with_xsd(XML_OUTPUT_PATH, XSD_PATH)

        if not is_valid:
            print(f"\n❌ Le fichier XML n'est pas conforme au schéma XSD")
            print(f"   {len(errors)} erreur(s) détectée(s)")
            return False

        print("✅ Validation XSD réussie.\n")

        # ==============================================
        # ÉTAPE 4 : TRANSFORMATION XSLT : XML → JSON
        # ==============================================
        print_banner("ÉTAPE 4 : TRANSFORMATION XML → JSON", "-")

        success, json_data = convert_xml_to_json(
            XML_OUTPUT_PATH,
            XSLT_JSON_PATH,
            JSON_OUTPUT_PATH
        )

        if not success or not json_data:
            print("❌ Échec de la conversion XML → JSON")
            return False

        print("✅ Conversion JSON réussie.\n")

        # ==============================================
        # ÉTAPE 5 : CONNEXION À MONGODB
        # ==============================================
        print_banner("ÉTAPE 5 : CONNEXION À MONGODB", "-")

        mongo_manager = MongoDBManager(
            host=MONGO_HOST,
            port=MONGO_PORT,
            database=MONGO_DATABASE
        )

        if not mongo_manager.connect():
            print("❌ Impossible de se connecter à MongoDB")
            print(f"💡 Vérifiez que MongoDB est démarré sur {MONGO_HOST}:{MONGO_PORT}")
            return False

        print("✅ Connexion MongoDB établie.\n")

        try:
            # ==============================================
            # ÉTAPE 6 : INSERTION DANS MONGODB
            # ==============================================
            print_banner("ÉTAPE 6 : INSERTION DANS MONGODB", "-")

            success, count = mongo_manager.insert_spotify_playlists(
                json_data,
                clear_first=True
            )

            if not success:
                print("❌ Échec de l'insertion dans MongoDB")
                return False

            print(f"\n✅ {count} playlists insérées avec succès.\n")

            # ==============================================
            # ÉTAPE 7 : VÉRIFICATION DES DONNÉES
            # ==============================================
            print_banner("ÉTAPE 7 : VÉRIFICATION DES DONNÉES", "-")

            # Récupérer les statistiques
            stats = mongo_manager.get_collection_stats('playlists')

            if stats:
                print("\n📊 Récapitulatif :")
                print("-" * 70)
                print(f"  • Base de données    : {MONGO_DATABASE}")
                print(f"  • Collection         : playlists")
                print(f"  • Documents insérés  : {count}")
                print(f"  • Taille totale      : {stats['size']/1024:.2f} KB")
                print("-" * 70 + "\n")

            # Afficher quelques exemples
            print("📋 Exemples de playlists insérées :")
            print("-" * 70)

            playlists = mongo_manager.query_playlists(limit=3)

            for i, playlist in enumerate(playlists, 1):
                print(f"\n  {i}. {playlist.get('nom', 'N/A')}")
                print(f"     • Genre : {playlist.get('genre', 'N/A')}")
                print(f"     • Subgenre : {playlist.get('subgenre', 'N/A')}")
                print(f"     • Tracks : {len(playlist.get('tracks', []))}")

            print("\n" + "-" * 70 + "\n")

            print_banner("✅ PIPELINE MONGODB TERMINÉ AVEC SUCCÈS ✅")

            return True

        finally:
            # Fermeture de la connexion MongoDB
            mongo_manager.close()

    except KeyboardInterrupt:
        print("\n\n⚠️  Processus interrompu par l'utilisateur.")
        return False

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE : {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mongodb_connection():
    """Teste uniquement la connexion à MongoDB."""
    print_banner("🔌 TEST DE CONNEXION MONGODB 🔌")

    mongo_manager = MongoDBManager(
        host=MONGO_HOST,
        port=MONGO_PORT,
        database=MONGO_DATABASE
    )

    if mongo_manager.connect():
        print("✅ Connexion réussie !")

        # Lister les collections
        try:
            collections = mongo_manager.db.list_collection_names()
            if collections:
                print("\n📊 Collections détectées :")
                for collection in collections:
                    count = mongo_manager.db[collection].count_documents({})
                    print(f"  • {collection} : {count} documents")
            else:
                print("\nℹ️  Aucune collection détectée (base vide).")
        except Exception as e:
            print(f"\n⚠️  Erreur lors de la récupération des collections : {e}")

        mongo_manager.close()
        return True
    else:
        print("❌ Échec de la connexion.")
        print(f"💡 Vérifiez que MongoDB est démarré sur {MONGO_HOST}:{MONGO_PORT}")
        return False


def main():
    """
    Fonction principale avec gestion des arguments en ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Pipeline de données Spotify : CSV → Oracle → XML → HTML & MongoDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation :

  PIPELINE 1 : CSV → Oracle → XML → HTML
  ==========================================
  # Ingestion complète (drop + create + insert)
  python main.py --full-reset

  # Ingestion sans suppression des tables
  python main.py --initialize

  # Insertion seule (tables déjà créées)
  python main.py

  # Export XML uniquement
  python main.py --export-xml

  # Test de connexion Oracle
  python main.py --test-connection

  PIPELINE 2 : XML → XSD → JSON → MongoDB
  ==========================================
  # Pipeline MongoDB complet
  python main.py --mongodb-pipeline

  # Test de connexion MongoDB
  python main.py --test-mongodb
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

    parser.add_argument(
        '--mongodb-pipeline',
        action='store_true',
        help='Exécute le pipeline MongoDB : XML → XSD → JSON → MongoDB'
    )

    parser.add_argument(
        '--test-mongodb',
        action='store_true',
        help='Teste uniquement la connexion à MongoDB'
    )

    args = parser.parse_args()

    # Traitement des arguments
    if args.test_connection:
        success = test_connection()
    elif args.test_mongodb:
        success = test_mongodb_connection()
    elif args.mongodb_pipeline:
        success = run_mongodb_pipeline()
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
"""
Module de gestion de la base de données MongoDB pour les données Spotify.
Gère la connexion, l'insertion et les requêtes sur MongoDB.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, BulkWriteError
import json
from pathlib import Path


class MongoDBManager:
    """
    Gère la connexion à MongoDB et les opérations CRUD.
    """

    def __init__(self, host='localhost', port=27017, database='spotify_db'):
        """
        Initialise le gestionnaire MongoDB.

        Args:
            host: Hôte MongoDB (défaut: localhost)
            port: Port MongoDB (défaut: 27017)
            database: Nom de la base de données (défaut: spotify_db)
        """
        self.host = host
        self.port = port
        self.database_name = database
        self.client = None
        self.db = None

    def connect(self):
        """
        Établit la connexion à MongoDB.

        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Créer le client MongoDB avec un timeout
            self.client = MongoClient(
                host=self.host,
                port=self.port,
                serverSelectionTimeoutMS=5000  # Timeout de 5 secondes
            )

            # Vérifier la connexion
            self.client.admin.command('ping')

            # Sélectionner la base de données
            self.db = self.client[self.database_name]

            print("✅ Connexion à MongoDB établie.")
            print(f"   Hôte         : {self.host}:{self.port}")
            print(f"   Base de données : {self.database_name}")
            print(f"   Version MongoDB : {self.client.server_info()['version']}")

            return True

        except ConnectionFailure as e:
            print(f"❌ Erreur de connexion à MongoDB : {e}")
            print(f"💡 Vérifiez que MongoDB est démarré sur {self.host}:{self.port}")
            self.client = None
            self.db = None
            return False

        except Exception as e:
            print(f"❌ Erreur inattendue lors de la connexion : {e}")
            self.client = None
            self.db = None
            return False

    def close(self):
        """Ferme la connexion à MongoDB."""
        if self.client:
            try:
                self.client.close()
                print("✅ Connexion à MongoDB fermée.")
            except Exception as e:
                print(f"⚠️  Erreur lors de la fermeture : {e}")
            finally:
                self.client = None
                self.db = None

    def __enter__(self):
        """Support du context manager (with statement)."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fermeture automatique avec context manager."""
        self.close()

    def test_connection(self):
        """
        Test la connexion à MongoDB.

        Returns:
            bool: True si la connexion est active
        """
        if not self.client:
            return False

        try:
            self.client.admin.command('ping')
            print("✅ Connexion MongoDB active.")
            return True
        except Exception as e:
            print(f"❌ Connexion MongoDB inactive : {e}")
            return False

    def drop_collection(self, collection_name):
        """
        Supprime une collection.

        Args:
            collection_name: Nom de la collection à supprimer

        Returns:
            bool: True si succès
        """
        if self.db is None:
            print("❌ Pas de connexion active à MongoDB.")
            return False

        try:
            self.db[collection_name].drop()
            print(f"✅ Collection '{collection_name}' supprimée.")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la suppression de la collection : {e}")
            return False

    def insert_json_data(self, collection_name, json_data, clear_first=False):
        """
        Insère des données JSON dans une collection MongoDB.

        Args:
            collection_name: Nom de la collection
            json_data: Données JSON (dict ou list)
            clear_first: Si True, supprime la collection avant insertion

        Returns:
            tuple: (bool: succès, int: nombre de documents insérés)
        """
        if self.db is None:
            print("❌ Pas de connexion active à MongoDB.")
            return False, 0

        print(f"\n💾 Insertion dans MongoDB...")
        print(f"   Collection : {collection_name}")

        try:
            collection = self.db[collection_name]

            # Supprimer la collection si demandé
            if clear_first:
                print(f"   ⚠️  Suppression de la collection existante...")
                collection.drop()
                collection = self.db[collection_name]

            # Compter les documents existants
            count_before = collection.count_documents({})
            print(f"   Documents existants : {count_before}")

            # Insérer les données
            inserted_count = 0

            if isinstance(json_data, dict):
                # Si c'est un seul document
                result = collection.insert_one(json_data)
                if result.inserted_id:
                    inserted_count = 1
                    print(f"   ✅ Document inséré avec ID : {result.inserted_id}")

            elif isinstance(json_data, list):
                # Si c'est une liste de documents
                if not json_data:
                    print("   ⚠️  Aucune donnée à insérer.")
                    return True, 0

                result = collection.insert_many(json_data, ordered=False)
                inserted_count = len(result.inserted_ids)
                print(f"   ✅ {inserted_count} documents insérés.")

            else:
                print("   ❌ Type de données non supporté. Attendu : dict ou list")
                return False, 0

            # Compter les documents après insertion
            count_after = collection.count_documents({})
            print(f"   Documents totaux : {count_after}")

            return True, inserted_count

        except DuplicateKeyError as e:
            print(f"❌ Erreur : Document(s) avec clé dupliquée : {e}")
            return False, 0

        except BulkWriteError as e:
            print(f"⚠️  Erreur partielle lors de l'insertion en masse :")
            print(f"   Insérés : {e.details.get('nInserted', 0)}")
            print(f"   Erreurs : {len(e.details.get('writeErrors', []))}")
            return False, e.details.get('nInserted', 0)

        except Exception as e:
            print(f"❌ Erreur lors de l'insertion : {e}")
            import traceback
            traceback.print_exc()
            return False, 0

    def insert_spotify_playlists(self, json_data, clear_first=True):
        """
        Insère les playlists Spotify dans MongoDB.

        Args:
            json_data: Données JSON Spotify (format : {playlists: [...], ...})
            clear_first: Si True, supprime la collection avant insertion

        Returns:
            tuple: (bool: succès, int: nombre de playlists insérées)
        """
        if self.db is None:
            print("❌ Pas de connexion active à MongoDB.")
            return False, 0

        print("\n" + "="*70)
        print(" 💾 INSERTION DES PLAYLISTS SPOTIFY DANS MONGODB")
        print("="*70)

        try:
            # Extraire les playlists
            if not isinstance(json_data, dict):
                print("❌ Format JSON invalide. Attendu : dict avec clé 'playlists'")
                return False, 0

            playlists = json_data.get('playlists', [])

            if not playlists:
                print("⚠️  Aucune playlist trouvée dans les données JSON.")
                return False, 0

            print(f"\n📊 Données à insérer :")
            print(f"   • Playlists : {len(playlists)}")

            total_tracks = sum(len(p.get('tracks', [])) for p in playlists)
            print(f"   • Tracks totaux : {total_tracks}")

            # Ajouter les métadonnées à chaque playlist
            for playlist in playlists:
                playlist['_metadata'] = {
                    'generated_at': json_data.get('generated_at'),
                    'source': 'spotify_xml_export'
                }

            # Insérer dans la collection 'playlists'
            success, count = self.insert_json_data('playlists', playlists, clear_first=clear_first)

            if success:
                print("\n" + "="*70)
                print(" ✅ INSERTION RÉUSSIE")
                print("="*70)
                print(f"\n📊 Résumé :")
                print(f"   • Collection : playlists")
                print(f"   • Documents insérés : {count}")
                print(f"   • Tracks totaux : {total_tracks}")

                # Créer un index sur l'ID de playlist
                self.create_index('playlists', 'id', unique=True)

                return True, count
            else:
                return False, 0

        except Exception as e:
            print(f"\n❌ Erreur lors de l'insertion des playlists : {e}")
            import traceback
            traceback.print_exc()
            return False, 0

    def create_index(self, collection_name, field_name, unique=False):
        """
        Crée un index sur un champ.

        Args:
            collection_name: Nom de la collection
            field_name: Nom du champ à indexer
            unique: Si True, l'index est unique

        Returns:
            bool: True si succès
        """
        if self.db is None:
            return False

        try:
            collection = self.db[collection_name]
            index_name = collection.create_index([(field_name, 1)], unique=unique)
            print(f"   ✅ Index créé sur '{field_name}' : {index_name}")
            return True
        except Exception as e:
            # Ne pas afficher d'erreur si l'index existe déjà
            if "already exists" not in str(e).lower():
                print(f"   ⚠️  Erreur lors de la création de l'index : {e}")
            return False

    def get_collection_stats(self, collection_name):
        """
        Récupère les statistiques d'une collection.

        Args:
            collection_name: Nom de la collection

        Returns:
            dict: Statistiques de la collection
        """
        if self.db is None:
            print("❌ Pas de connexion active à MongoDB.")
            return None

        try:
            collection = self.db[collection_name]

            stats = {
                'name': collection_name,
                'count': collection.count_documents({}),
                'indexes': collection.list_indexes(),
                'size': self.db.command("collstats", collection_name).get('size', 0)
            }

            print(f"\n📊 Statistiques de la collection '{collection_name}' :")
            print(f"   • Documents : {stats['count']}")
            print(f"   • Taille : {stats['size']:,} bytes ({stats['size']/1024:.2f} KB)")
            print(f"   • Index : {list(stats['indexes'])}")

            return stats

        except Exception as e:
            print(f"❌ Erreur lors de la récupération des statistiques : {e}")
            return None

    def query_playlists(self, filter_query=None, limit=10):
        """
        Récupère des playlists avec un filtre optionnel.

        Args:
            filter_query: Filtre MongoDB (dict)
            limit: Nombre maximum de documents à retourner

        Returns:
            list: Liste des playlists
        """
        if self.db is None:
            print("❌ Pas de connexion active à MongoDB.")
            return []

        try:
            collection = self.db['playlists']
            filter_query = filter_query or {}

            playlists = list(collection.find(filter_query).limit(limit))

            print(f"\n📋 Requête MongoDB :")
            print(f"   • Filtre : {filter_query}")
            print(f"   • Résultats : {len(playlists)} playlist(s)")

            return playlists

        except Exception as e:
            print(f"❌ Erreur lors de la requête : {e}")
            return []


# Test du module
if __name__ == "__main__":
    print("🧪 Test du module mongodb_manager")
    print("="*70)

    # Test de connexion
    with MongoDBManager(host='localhost', port=27017, database='spotify_db') as mongo:
        if mongo.test_connection():
            print("\n✅ Test de connexion réussi !")

            # Test d'insertion avec des données de test
            test_data = {
                "generated_at": "2025-12-04T00:00:00",
                "total_playlists": 1,
                "total_tracks": 1,
                "playlists": [
                    {
                        "id": "test123",
                        "nom": "Test Playlist",
                        "genre": "test",
                        "subgenre": "test",
                        "tracks_count": 1,
                        "tracks": [
                            {
                                "id": "track123",
                                "name": "Test Track",
                                "duration_ms": 180000,
                                "popularity": 50
                            }
                        ]
                    }
                ]
            }

            print("\n📝 Test d'insertion de données...")
            success, count = mongo.insert_spotify_playlists(test_data, clear_first=True)

            if success:
                print(f"✅ {count} playlist(s) insérée(s)")

                # Récupérer les statistiques
                mongo.get_collection_stats('playlists')

                # Nettoyer
                mongo.drop_collection('playlists')
                print("\n🧹 Collection de test nettoyée")
        else:
            print("\n❌ Test de connexion échoué")
            print("💡 Assurez-vous que MongoDB est démarré")

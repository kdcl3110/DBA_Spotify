# Fichier : db_manager.py

import oracledb
from configs import DB_USER, DB_PASSWORD, DB_DSN
from .db_schema import CREATE_TABLES_SQL, DROP_TABLES_SQL
import pandas as pd
from datetime import datetime

class DatabaseManager:
    """
    Gère la connexion à la base de données Oracle et les opérations DDL/DML/Query.
    """
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Établit et retourne la connexion à la base de données."""
        try:
            self.connection = oracledb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=DB_DSN
            )
            print("✅ Connexion à la base de données Oracle établie.")
            print(f"   Version Oracle : {self.connection.version}")
            return True
        except oracledb.Error as e:
            error_obj, = e.args
            print(f"❌ Erreur de connexion à Oracle : {error_obj.message}")
            self.connection = None
            return False

    def close(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            try:
                self.connection.close()
                print("✅ Connexion à la base de données fermée.")
            except Exception as e:
                print(f"⚠️ Erreur lors de la fermeture : {e}")
            finally:
                self.connection = None
    
    def __enter__(self):
        """Support du context manager (with statement)."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fermeture automatique avec context manager."""
        self.close()

    def _execute_sql_script(self, sql_script, commit=False):
        """
        Exécute un script SQL contenant plusieurs statements séparés par des points-virgules.
        Gère les erreurs pour chaque statement individuellement.
        """
        if not self.connection:
            print("❌ Pas de connexion active.")
            return False
        
        cursor = self.connection.cursor()
        success_count = 0
        error_count = 0
        
        try:
            # Séparer les statements (attention aux ; dans les chaînes)
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements, 1):
                try:
                    cursor.execute(statement)
                    success_count += 1
                except oracledb.Error as e:
                    error_count += 1
                    # Ne pas afficher l'erreur "table does not exist" lors du DROP
                    if "does not exist" not in str(e).lower():
                        print(f"   ⚠️ Statement {i} : {str(e)[:100]}")
            
            if commit:
                self.connection.commit()
            
            return error_count == 0
        
        except Exception as e:
            print(f"❌ Erreur globale lors de l'exécution du script : {e}")
            if commit:
                self.connection.rollback()
            return False
        finally:
            cursor.close()

    def initialize_db(self, drop_first=False):
        """Crée toutes les tables si elles n'existent pas (option de suppression)."""
        if not self.connection:
            print("❌ Pas de connexion active.")
            return False

        if drop_first:
            print("\n⚠️  Suppression des tables existantes...")
            for drop_sql in DROP_TABLES_SQL:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(drop_sql)
                    self.connection.commit()
                    print(f"   ✓ Table supprimée")
                except oracledb.Error as e:
                    # Ignorer l'erreur si la table n'existe pas
                    if "does not exist" not in str(e).lower():
                        print(f"   ⚠️ Erreur DROP : {e}")
                finally:
                    cursor.close()
            print("✅ Suppression terminée.\n")
        
        print("⚙️  Création des tables de la BD Spotify...")
        
        # Exécuter le script de création
        if self._execute_sql_script(CREATE_TABLES_SQL, commit=True):
            print("✅ Initialisation du schéma de base de données terminée.\n")
            return True
        else:
            print("⚠️ Initialisation terminée avec des avertissements.\n")
            return False

    def _execute_many(self, sql_query, data_list):
        """
        Exécute une insertion de masse (executemany) pour les tables SANS colonne IDENTITY.
        Retourne le nombre de lignes insérées.
        """
        if not self.connection:
            return 0
        
        if not data_list:
            return 0
        
        cursor = self.connection.cursor()
        try:
            cursor.executemany(sql_query, data_list)
            self.connection.commit()
            rows_inserted = cursor.rowcount
            return rows_inserted
        except oracledb.Error as e:
            print(f"❌ Erreur SQL lors de l'insertion (executemany): {e}")
            print(f"   Première ligne de données : {data_list[0] if data_list else 'N/A'}")
            self.connection.rollback()
            return 0
        finally:
            cursor.close()

    def _insert_with_identity(self, table_name, df, columns, id_col):
        """
        Insère ligne par ligne dans une table avec IDENTITY et récupère les IDs générés.
        
        Args:
            table_name: Nom de la table
            df: DataFrame contenant les données
            columns: Liste des colonnes à insérer (sans l'ID)
            id_col: Nom de la colonne ID à récupérer
            
        Returns:
            Dictionnaire mappant les valeurs vers leurs IDs générés
        """
        if not self.connection or df.empty:
            return {}
        
        cursor = self.connection.cursor()
        
        # Construction de la requête SQL
        placeholders = ', '.join([f':{i+1}' for i in range(len(columns))])
        sql_insert = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) RETURNING {id_col} INTO :{len(columns)+1}"
        
        id_map = {}
        rows_inserted = 0
        
        try:
            for index, row in df.iterrows():
                # Extraire les valeurs pour cette ligne
                values = [row[col] for col in columns]
                
                # Variable pour récupérer l'ID généré
                new_id_var = cursor.var(oracledb.NUMBER)
                
                # Exécuter l'insertion
                cursor.execute(sql_insert, values + [new_id_var])
                
                # Récupérer l'ID généré
                generated_id = new_id_var.getvalue()[0]
                
                # Mapper la première colonne (clé naturelle) vers l'ID
                key = row[columns[0]]
                id_map[key] = int(generated_id)
                
                rows_inserted += 1
            
            self.connection.commit()
            print(f"   → {rows_inserted} lignes insérées avec mapping des IDs")
            
            return id_map
        
        except oracledb.Error as e:
            print(f"❌ Erreur lors de l'insertion dans {table_name}: {e}")
            self.connection.rollback()
            return {}
        finally:
            cursor.close()

    def _parse_date_for_oracle(self, date_str):
        """
        Convertit une chaîne de date en objet datetime.date pour Oracle.
        Gère les formats : YYYY-MM-DD, YYYY-MM, YYYY
        """
        if pd.isna(date_str) or date_str is None or date_str == '':
            return None
        
        date_str = str(date_str).strip()
        
        try:
            # Format complet YYYY-MM-DD
            if len(date_str) == 10:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            # Format YYYY-MM
            elif len(date_str) == 7:
                return datetime.strptime(date_str + '-01', '%Y-%m-%d').date()
            # Format YYYY seulement
            elif len(date_str) == 4:
                return datetime.strptime(date_str + '-01-01', '%Y-%m-%d').date()
            else:
                return None
        except:
            return None

    def insert_data(self, data_dict):
        """
        Insère les données normalisées dans les tables dans l'ordre de dépendance.
        Gère les clés étrangères et les tables IDENTITY.
        """
        if not self.connection:
            print("❌ Pas de connexion active.")
            return False

        print("\n" + "="*60)
        print("🚀 DÉMARRAGE DE L'INSERTION DES DONNÉES NORMALISÉES")
        print("="*60 + "\n")
        
        try:
            # ========================================
            # PHASE 1 : TABLES PARENTES AVEC IDENTITY
            # ========================================
            
            # 1. sp_genres (table parente, IDENTITY)
            print("1️⃣  Insertion des GENRES (IDENTITY)...")
            genres_map = self._insert_with_identity(
                'sp_genres',
                data_dict['sp_genres'],
                ['nom_genre'],
                'id_genre'
            )
            
            # 2. sp_artists (table parente, IDENTITY)
            print("\n2️⃣  Insertion des ARTISTES (IDENTITY)...")
            artists_map = self._insert_with_identity(
                'sp_artists',
                data_dict['sp_artists'],
                ['nom_artist'],
                'id_artist'
            )
            
            # ========================================
            # PHASE 2 : TABLES ENFANTS AVEC FK
            # ========================================
            
            # 3. sp_subgenres (IDENTITY + FK vers genres)
            print("\n3️⃣  Insertion des SOUS-GENRES (IDENTITY + FK genre)...")
            subgenres_df = data_dict['sp_subgenres'].copy()
            
            # Mapper les noms de genres vers leurs IDs
            subgenres_df['id_genre'] = subgenres_df['nom_genre'].map(genres_map)
            
            # Filtrer les lignes sans ID de genre valide
            subgenres_df = subgenres_df.dropna(subset=['id_genre'])
            subgenres_df['id_genre'] = subgenres_df['id_genre'].astype(int)
            
            subgenres_map = self._insert_with_identity(
                'sp_subgenres',
                subgenres_df,
                ['nom_subgenre', 'id_genre'],
                'id_subgenre'
            )
            
            # 4. sp_albums (FK vers artists)
            print("\n4️⃣  Insertion des ALBUMS (FK artiste)...")
            albums_df = data_dict['sp_albums'].copy()
            
            # Mapper les noms d'artistes vers leurs IDs
            albums_df['id_artist'] = albums_df['artiste_principal'].map(artists_map)
            
            # Filtrer les albums sans artiste valide
            albums_df = albums_df.dropna(subset=['id_artist', 'id_album'])
            albums_df['id_artist'] = albums_df['id_artist'].astype(int)
            
            # Convertir les dates
            albums_df['date_sortie_oracle'] = albums_df['date_sortie'].apply(self._parse_date_for_oracle)
            
            # Préparer les données pour l'insertion
            sql_album = "INSERT INTO sp_albums (id_album, nom_album, date_sortie, id_artist) VALUES (:1, :2, :3, :4)"
            albums_data = albums_df[['id_album', 'nom_album', 'date_sortie_oracle', 'id_artist']].values.tolist()
            
            rows_inserted = self._execute_many(sql_album, albums_data)
            print(f"   → {rows_inserted} albums insérés")
            
            # Garder seulement les albums insérés pour les FK suivantes
            valid_albums = set(albums_df['id_album'])
            
            # 5. sp_tracks (FK vers albums)
            print("\n5️⃣  Insertion des PISTES (FK album)...")
            tracks_df = data_dict['sp_tracks'].copy()
            
            # Filtrer les tracks dont l'album existe
            tracks_df = tracks_df[tracks_df['id_album'].isin(valid_albums)]
            tracks_df = tracks_df.dropna(subset=['id_track', 'id_album'])
            
            sql_track = "INSERT INTO sp_tracks (id_track, track_name, duration_ms, track_popularity, id_album) VALUES (:1, :2, :3, :4, :5)"
            tracks_data = tracks_df[['id_track', 'nom_track', 'duration_ms', 'track_popularity', 'id_album']].values.tolist()
            
            rows_inserted = self._execute_many(sql_track, tracks_data)
            print(f"   → {rows_inserted} pistes insérées")
            
            # Garder les tracks valides pour les FK suivantes
            valid_tracks = set(tracks_df['id_track'])
            
            # 6. sp_audio_features (FK vers tracks)
            print("\n6️⃣  Insertion des CARACTÉRISTIQUES AUDIO (FK piste)...")
            audio_df = data_dict['sp_audio_features'].copy()
            
            # Filtrer les features dont la track existe
            audio_df = audio_df[audio_df['id_track'].isin(valid_tracks)]
            audio_df = audio_df.dropna(subset=['id_track'])
            
            # Colonnes à insérer
            audio_cols = ['id_track', 'energy', 'tempo', 'danceability', 'loudness', 
                         'liveness', 'valence', 'speechiness', 'acousticness', 
                         'instrumentalness', 'key_musical', 'mode_musical', 'time_signature']
            
            # Vérifier si analysis_url existe
            if 'analysis_url' in audio_df.columns:
                audio_cols.append('analysis_url')
            
            sql_audio = f"INSERT INTO sp_audio_features ({', '.join(audio_cols)}) VALUES ({', '.join([f':{i+1}' for i in range(len(audio_cols))])})"
            audio_data = audio_df[audio_cols].values.tolist()
            
            rows_inserted = self._execute_many(sql_audio, audio_data)
            print(f"   → {rows_inserted} caractéristiques audio insérées")
            
            # 7. sp_playlists (FK vers subgenres)
            print("\n7️⃣  Insertion des PLAYLISTS (FK sous-genre)...")
            playlists_df = data_dict['sp_playlists'].copy()
            
            # Mapper les noms de sous-genres vers leurs IDs
            playlists_df['id_subgenre'] = playlists_df['nom_subgenre'].map(subgenres_map)
            
            # Filtrer les playlists sans sous-genre valide
            playlists_df = playlists_df.dropna(subset=['id_subgenre', 'id_playlist'])
            playlists_df['id_subgenre'] = playlists_df['id_subgenre'].astype(int)
            
            sql_playlist = "INSERT INTO sp_playlists (id_playlist, nom_playlist, id_subgenre) VALUES (:1, :2, :3)"
            playlists_data = playlists_df[['id_playlist', 'nom_playlist', 'id_subgenre']].values.tolist()
            
            rows_inserted = self._execute_many(sql_playlist, playlists_data)
            print(f"   → {rows_inserted} playlists insérées")
            
            # Garder les playlists valides
            valid_playlists = set(playlists_df['id_playlist'])
            
            # 8. sp_playlist_tracks (table de liaison, FK vers playlists et tracks)
            print("\n8️⃣  Insertion des LIAISONS PLAYLIST-TRACK...")
            pt_df = data_dict['sp_playlist_tracks'].copy()
            
            # Filtrer pour ne garder que les liaisons valides
            pt_df = pt_df[
                pt_df['id_playlist'].isin(valid_playlists) &
                pt_df['id_track'].isin(valid_tracks)
            ]
            
            sql_pt = "INSERT INTO sp_playlist_tracks (id_playlist, id_track) VALUES (:1, :2)"
            pt_data = pt_df[['id_playlist', 'id_track']].values.tolist()
            
            rows_inserted = self._execute_many(sql_pt, pt_data)
            print(f"   → {rows_inserted} liaisons insérées")
            
            print("\n" + "="*60)
            print("✅ INSERTION DE TOUTES LES DONNÉES TERMINÉE AVEC SUCCÈS")
            print("="*60 + "\n")
            
            return True
        
        except Exception as e:
            print(f"\n❌ ERREUR CRITIQUE lors de l'insertion : {e}")
            import traceback
            traceback.print_exc()
            if self.connection:
                self.connection.rollback()
            return False

    def fetch_data_for_xml(self):
        """
        Extrait les données complètes de la BD pour la génération XML.
        Joint toutes les tables nécessaires.
        
        Returns:
            Liste de dictionnaires contenant toutes les données jointes
        """
        if not self.connection:
            print("❌ Pas de connexion active.")
            return []
        
        print("\n🔍 Extraction des données pour export XML...")
        
        # Requête complexe avec toutes les jointures
        SQL_QUERY = """
            SELECT
                p.id_playlist,
                p.nom_playlist,
                sg.nom_subgenre,
                g.nom_genre,
                t.id_track,
                t.track_name,
                t.duration_ms,
                t.track_popularity,
                a.id_album,
                a.nom_album,
                TO_CHAR(a.date_sortie, 'YYYY-MM-DD') as date_sortie,
                ar.nom_artist as artiste_principal,
                af.energy,
                af.tempo,
                af.danceability,
                af.loudness,
                af.valence,
                af.liveness,
                af.speechiness,
                af.acousticness,
                af.instrumentalness
            FROM sp_playlists p
            INNER JOIN sp_subgenres sg ON p.id_subgenre = sg.id_subgenre
            INNER JOIN sp_genres g ON sg.id_genre = g.id_genre
            INNER JOIN sp_playlist_tracks pt ON p.id_playlist = pt.id_playlist
            INNER JOIN sp_tracks t ON pt.id_track = t.id_track
            INNER JOIN sp_albums a ON t.id_album = a.id_album
            INNER JOIN sp_artists ar ON a.id_artist = ar.id_artist
            LEFT JOIN sp_audio_features af ON t.id_track = af.id_track
            ORDER BY p.id_playlist, t.track_name
        """
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(SQL_QUERY)
            
            # Récupérer les noms de colonnes
            cols = [col[0].lower() for col in cursor.description]
            
            # Construire la liste de dictionnaires
            results = []
            for row in cursor.fetchall():
                row_dict = {}
                for col, val in zip(cols, row):
                    # Convertir les valeurs None en chaînes vides pour XML
                    row_dict[col] = val if val is not None else ''
                results.append(row_dict)
            
            print(f"✅ Extraction terminée : {len(results)} lignes récupérées\n")
            return results
        
        except oracledb.Error as e:
            print(f"❌ Erreur SQL lors de l'extraction : {e}")
            return []
        finally:
            cursor.close()

    def get_statistics(self):
        """
        Retourne des statistiques sur les données en base.
        """
        if not self.connection:
            return None
        
        stats = {}
        tables = [
            'sp_genres', 'sp_subgenres', 'sp_artists', 'sp_albums',
            'sp_tracks', 'sp_audio_features', 'sp_playlists', 'sp_playlist_tracks'
        ]
        
        cursor = self.connection.cursor()
        try:
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats[table] = count
            
            return stats
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des statistiques : {e}")
            return None
        finally:
            cursor.close()
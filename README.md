# Spotify Analytics Pipeline

Pipeline complet d'analyse de données Spotify : extraction CSV, stockage Oracle, export XML et génération de dashboard HTML interactif.

## Description

Ce projet implémente un pipeline ETL (Extract, Transform, Load) pour analyser des données de playlists Spotify. Les données sont extraites d'un fichier CSV, normalisées, stockées dans une base de données Oracle, exportées en XML avec validation DTD, puis transformées en un dashboard HTML interactif via XSLT.

## Fonctionnalités

- **Extraction et normalisation** : Lecture et traitement des données CSV Spotify
- **Stockage Oracle** : Insertion des données dans une base de données relationnelle Oracle
- **Export XML** : Génération d'un fichier XML structuré à partir des données
- **Validation DTD** : Création automatique et validation de la structure XML
- **Transformation XSLT** : Génération d'un dashboard HTML avec graphiques interactifs
- **Dashboard Analytics** : Visualisation des playlists, tracks et caractéristiques audio

## Structure du Projet

```
DBA_Spotify/
├── main.py                      # Point d'entrée principal
├── requirements.txt             # Dépendances Python
├── configs/
│   └── config.py               # Configuration (DB, chemins)
├── DB/
│   ├── db_manager.py           # Gestionnaire de base de données Oracle
│   ├── db_schema.py            # Schéma des tables
│   └── models.py               # Modèles de données
├── services/
│   ├── data_processor.py       # Traitement et normalisation CSV
│   ├── xml_exporter.py         # Export vers XML
│   ├── dtd_creator.py          # Génération de DTD
│   ├── dtd_validator.py        # Validation DTD
│   └── xslt_transformer.py     # Transformation XSLT → HTML
└── data/
    ├── input/
    │   ├── high_popularity_spotify_data.csv    # Données source
    │   └── spotify_transform.xslt              # Template XSLT
    └── output/
        ├── spotify_data_export.xml             # XML généré
        ├── spotify_data.dtd                    # DTD généré
        └── spotify_data.html                   # Dashboard HTML
```

## Prérequis

- **Python** : 3.8 ou supérieur
- **Oracle Database** : 11g ou supérieur (ou Oracle XE)
- **Oracle Instant Client** : Installé et configuré

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/DBA_Spotify.git
cd DBA_Spotify
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données Oracle

#### Créer l'utilisateur et le tablespace (SQL*Plus ou SQL Developer)

```sql
-- Se connecter en tant que SYSDBA
sqlplus sys as sysdba

-- Créer le tablespace
CREATE TABLESPACE spotify_data
DATAFILE 'spotify_data.dbf' SIZE 100M
AUTOEXTEND ON NEXT 10M MAXSIZE UNLIMITED;

-- Créer l'utilisateur
CREATE USER spotify_user IDENTIFIED BY spotify123
DEFAULT TABLESPACE spotify_data
TEMPORARY TABLESPACE temp
QUOTA UNLIMITED ON spotify_data;

-- Accorder les privilèges
GRANT CONNECT, RESOURCE TO spotify_user;
GRANT CREATE TABLE, CREATE VIEW, CREATE SEQUENCE TO spotify_user;
```

## Configuration

### Variables d'environnement (recommandé)

Créez un fichier `.env` ou configurez les variables d'environnement :

```bash
# Windows PowerShell
$env:DB_USER="spotify_user"
$env:DB_PASSWORD="spotify123"
$env:DB_DSN="localhost:1521/XEPDB1"

# Linux/Mac
export DB_USER="spotify_user"
export DB_PASSWORD="spotify123"
export DB_DSN="localhost:1521/XEPDB1"
```

### Modification du fichier config.py

Alternativement, modifiez directement `configs/config.py` :

```python
DB_USER = "spotify_user"
DB_PASSWORD = "spotify123"
DB_DSN = "localhost:1521/XEPDB1"
```

## Utilisation

### Test de connexion

Vérifiez que la connexion à Oracle fonctionne :

```bash
python main.py --test-connection
```

### Pipeline complet (recommandé pour la première exécution)

Supprime et recrée toutes les tables, puis insère les données :

```bash
python main.py --full-reset
```

### Initialisation sans suppression

Crée les tables si elles n'existent pas (sans supprimer les données existantes) :

```bash
python main.py --initialize
```

### Insertion seule

Insère les données dans des tables déjà créées :

```bash
python main.py
```

### Export XML uniquement

Exporte les données existantes de la base vers XML (utile si les données sont déjà en base) :

```bash
python main.py --export-xml
```

## Workflow du Pipeline

Le pipeline s'exécute dans l'ordre suivant :

1. **Extraction CSV** : Lecture du fichier `high_popularity_spotify_data.csv`
2. **Normalisation** : Transformation des données en format relationnel
3. **Connexion Oracle** : Établissement de la connexion à la base de données
4. **Initialisation BD** : Création des tables (si nécessaire)
5. **Insertion** : Insertion des données normalisées
6. **Export XML** : Génération du fichier XML structuré
7. **Création DTD** : Génération automatique de la DTD
8. **Validation** : Validation du XML contre la DTD
9. **Transformation XSLT** : Génération du dashboard HTML
10. **Résultat** : Dashboard HTML interactif avec graphiques

## Résultats Générés

Après exécution, vous trouverez dans `data/output/` :

- `spotify_data_export.xml` : Données au format XML
- `spotify_data.dtd` : Définition de type de document
- `spotify_data.html` : Dashboard HTML avec graphiques Chart.js
- `test_DTD_DOCUMENTATION.txt` : Documentation de la structure DTD

## Dashboard HTML

Le dashboard généré comprend :

- Statistiques globales (nombre de playlists, tracks)
- Graphique de distribution des playlists
- Graphique de popularité moyenne par playlist
- Radar des caractéristiques audio moyennes
- Distribution des genres musicaux
- Liste détaillée des playlists avec leurs tracks
- Caractéristiques audio de chaque track (energy, danceability, valence, tempo, loudness)

Ouvrez `data/output/spotify_data.html` dans votre navigateur pour visualiser le dashboard.

## Technologies Utilisées

- **Python 3.8+**
- **pandas** : Manipulation de données
- **oracledb** : Connexion à Oracle Database
- **lxml** : Traitement XML/DTD/XSLT
- **Oracle Database** : Stockage relationnel
- **XSLT 1.0** : Transformation XML → HTML
- **Chart.js** : Graphiques interactifs dans le dashboard

## Structure de la Base de Données

Le schéma Oracle comprend les tables suivantes :

- `sp_genres` : Genres musicaux
- `sp_subgenres` : Sous-genres musicaux
- `sp_playlists` : Playlists Spotify
- `sp_artists` : Artistes
- `sp_albums` : Albums
- `sp_tracks` : Morceaux de musique
- `sp_audio_features` : Caractéristiques audio des tracks
- `sp_playlist_tracks` : Relation playlists-tracks (table de jointure)

## Dépannage

### Erreur de connexion Oracle

- Vérifiez que Oracle Database est démarré
- Vérifiez les identifiants dans `config.py` ou les variables d'environnement
- Testez avec : `python main.py --test-connection`

### Erreur "ORA-12154: TNS"

- Vérifiez le format du DSN : `host:port/service_name`
- Exemple : `localhost:1521/XEPDB1`

### Tables déjà existantes

- Utilisez `--full-reset` pour supprimer et recréer les tables

### Fichier CSV introuvable

- Vérifiez que `data/input/high_popularity_spotify_data.csv` existe
- Vérifiez les permissions de lecture

## Améliorations Futures

- Interface web pour visualiser les données en temps réel
- API REST pour accéder aux données
- Intégration avec l'API Spotify officielle
- Export vers d'autres formats (JSON, Parquet)
- Dashboard interactif avec filtres dynamiques

## Auteur

Cash

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

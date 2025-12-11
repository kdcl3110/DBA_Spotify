# Spotify Analytics Pipeline

Pipelines complets d'analyse de données Spotify avec double architecture : Oracle + MongoDB.

## Description

Ce projet implémente **deux pipelines ETL complémentaires** pour analyser des données de playlists Spotify :

### Pipeline 1 : CSV → Oracle → XML → HTML
Les données sont extraites d'un fichier CSV, normalisées, stockées dans une base de données Oracle, exportées en XML avec validation DTD, puis transformées en un dashboard HTML interactif via XSLT.

### Pipeline 2 : XML → XSD → JSON → MongoDB (NOUVEAU)
Le fichier XML généré est validé avec un schéma XSD, transformé en JSON via XSLT, puis inséré dans une base de données MongoDB pour une analyse NoSQL flexible.

## Fonctionnalités

### Pipeline 1 (Oracle → HTML)
- **Extraction et normalisation** : Lecture et traitement des données CSV Spotify
- **Stockage Oracle** : Insertion des données dans une base de données relationnelle Oracle
- **Export XML** : Génération d'un fichier XML structuré à partir des données
- **Validation DTD** : Création automatique et validation de la structure XML
- **Transformation XSLT** : Génération d'un dashboard HTML avec graphiques interactifs
- **Dashboard Analytics** : Visualisation des playlists, tracks et caractéristiques audio

### Pipeline 2 (MongoDB)
- **Génération XSD** : Création automatique d'un schéma XML Schema Definition
- **Validation XSD** : Validation stricte du XML avec typage des données
- **Transformation XSLT → JSON** : Conversion XML vers JSON via XSLT
- **Stockage MongoDB** : Insertion des données dans une base NoSQL pour requêtes flexibles
- **Indexation** : Création automatique d'index sur les champs clés

## Structure du Projet

```
DBA_Spotify/
├── main.py                      # Point d'entrée principal (2 pipelines)
├── spotify_pipeline_demo.ipynb  # Jupyter Notebook de démonstration (NOUVEAU)
├── requirements.txt             # Dépendances Python
├── configs/
│   └── config.py               # Configuration (Oracle, MongoDB, chemins)
├── DB/
│   ├── db_manager.py           # Gestionnaire Oracle
│   ├── mongodb_manager.py      # Gestionnaire MongoDB (NOUVEAU)
│   ├── db_schema.py            # Schéma des tables Oracle
│   └── models.py               # Modèles de données
├── services/
│   ├── data_processor.py       # Traitement et normalisation CSV
│   ├── xml_exporter.py         # Export vers XML
│   ├── dtd_creator.py          # Génération de DTD
│   ├── dtd_validator.py        # Validation DTD
│   ├── xsd_creator.py          # Génération de XSD (NOUVEAU)
│   ├── xsd_validator.py        # Validation XSD (NOUVEAU)
│   ├── json_converter.py       # Conversion XML → JSON (NOUVEAU)
│   └── xslt_transformer.py     # Transformation XSLT → HTML
└── data/
    ├── input/
    │   ├── high_popularity_spotify_data.csv    # Données source
    │   ├── spotify_transform.xslt              # Template XSLT → HTML
    │   └── spotify_to_json.xslt                # Template XSLT → JSON (NOUVEAU)
    └── output/
        ├── spotify_data_export.xml             # XML généré
        ├── spotify_data.dtd                    # DTD généré
        ├── spotify_data.xsd                    # XSD généré (NOUVEAU)
        ├── spotify_data.json                   # JSON généré (NOUVEAU)
        └── spotify_data.html                   # Dashboard HTML
```

## Prérequis

### Pipeline 1 (Oracle → HTML)
- **Python** : 3.8 ou supérieur
- **Oracle Database** : 11g ou supérieur (ou Oracle XE)
- **Oracle Instant Client** : Installé et configuré

### Pipeline 2 (MongoDB)
- **Python** : 3.8 ou supérieur
- **MongoDB** : 4.0 ou supérieur
- **MongoDB en cours d'exécution** : sur localhost:27017 (par défaut)

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

### 🎓 Démonstration Interactive avec Jupyter Notebook (RECOMMANDÉ)

Pour une expérience d'apprentissage complète avec documentation et exécution pas à pas :

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer Jupyter Notebook
jupyter notebook spotify_pipeline_demo.ipynb
```

Le notebook inclut :
- 📖 Documentation complète des 2 pipelines
- ▶️ Exécution pas à pas de chaque étape
- 📊 Visualisations interactives des données
- 🔍 Exemples de requêtes MongoDB avancées
- 📈 Analyses statistiques avec graphiques

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

## Utilisation du Pipeline 2 (MongoDB)

### Prérequis pour le Pipeline MongoDB

1. **Installer MongoDB** :
   - Téléchargez MongoDB Community Server depuis [mongodb.com](https://www.mongodb.com/try/download/community)
   - Installez MongoDB sur votre système
   - Démarrez le service MongoDB

2. **Installer les dépendances Python** :
```bash
pip install -r requirements.txt
```

### Configuration MongoDB

Vous pouvez configurer les paramètres MongoDB via les variables d'environnement ou `configs/config.py` :

```bash
# Windows PowerShell
$env:MONGO_HOST="localhost"
$env:MONGO_PORT="27017"
$env:MONGO_DATABASE="spotify_db"

# Linux/Mac
export MONGO_HOST="localhost"
export MONGO_PORT="27017"
export MONGO_DATABASE="spotify_db"
```

### Exécution du Pipeline MongoDB

#### Test de connexion MongoDB

Vérifiez d'abord que MongoDB est accessible :

```bash
python main.py --test-mongodb
```

#### Pipeline complet MongoDB

Exécutez le pipeline complet : XML → XSD → JSON → MongoDB

```bash
python main.py --mongodb-pipeline
```

**Note importante** : Le fichier XML doit déjà exister. Si ce n'est pas le cas, exécutez d'abord le Pipeline 1 :

```bash
# 1. Générer le XML depuis Oracle
python main.py --full-reset

# 2. Exécuter le pipeline MongoDB
python main.py --mongodb-pipeline
```

### Workflow du Pipeline MongoDB

Le pipeline MongoDB s'exécute dans l'ordre suivant :

1. **Vérification XML** : Vérifie que le fichier XML existe
2. **Génération XSD** : Création du schéma XML Schema Definition
3. **Validation XSD** : Validation du XML avec typage strict
4. **Transformation XSLT** : Conversion XML → JSON via XSLT
5. **Connexion MongoDB** : Établissement de la connexion
6. **Insertion** : Insertion des playlists dans MongoDB
7. **Indexation** : Création d'index sur le champ 'id'
8. **Vérification** : Affichage des statistiques et exemples

### Résultats du Pipeline MongoDB

Après exécution, vous trouverez dans `data/output/` :

- `spotify_data.xsd` : Schéma XML Schema Definition
- `spotify_data.json` : Données au format JSON
- `XSD_DOCUMENTATION.txt` : Documentation du schéma XSD

Et dans MongoDB :
- **Base de données** : `spotify_db`
- **Collection** : `playlists`
- **Documents** : 72 playlists avec leurs tracks imbriqués

### Requêtes MongoDB

Une fois les données insérées, vous pouvez les interroger avec MongoDB Shell ou Compass :

```javascript
// Se connecter à la base
use spotify_db

// Compter les playlists
db.playlists.countDocuments()

// Trouver une playlist par genre
db.playlists.find({ genre: "latin" })

// Trouver les playlists avec plus de 20 tracks
db.playlists.find({ tracks_count: { $gt: 20 } })

// Rechercher par nom de playlist
db.playlists.find({ nom: /Cumbia/i })

// Agrégation : tracks les plus populaires
db.playlists.aggregate([
  { $unwind: "$tracks" },
  { $sort: { "tracks.popularity": -1 } },
  { $limit: 10 },
  { $project: {
      track_name: "$tracks.name",
      artist: "$tracks.artist.name",
      popularity: "$tracks.popularity"
  }}
])
```

## Workflow du Pipeline 1 (Oracle)

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

### Pipeline 1 (Oracle → HTML)
- **Python 3.8+**
- **pandas** : Manipulation de données
- **oracledb** : Connexion à Oracle Database
- **lxml** : Traitement XML/DTD/XSLT
- **Oracle Database** : Stockage relationnel
- **XSLT 1.0** : Transformation XML → HTML
- **Chart.js** : Graphiques interactifs dans le dashboard

### Pipeline 2 (MongoDB)
- **Python 3.8+**
- **lxml** : Traitement XML/XSD/XSLT
- **pymongo** : Driver Python pour MongoDB
- **MongoDB** : Base de données NoSQL orientée documents
- **XSLT 1.0** : Transformation XML → JSON
- **JSON** : Format d'échange de données

## Structure des Bases de Données

### Oracle (Relationnel)

Le schéma Oracle comprend les tables suivantes :

- `sp_genres` : Genres musicaux
- `sp_subgenres` : Sous-genres musicaux
- `sp_playlists` : Playlists Spotify
- `sp_artists` : Artistes
- `sp_albums` : Albums
- `sp_tracks` : Morceaux de musique
- `sp_audio_features` : Caractéristiques audio des tracks
- `sp_playlist_tracks` : Relation playlists-tracks (table de jointure)

### MongoDB (NoSQL)

Structure des documents dans la collection `playlists` :

```json
{
  "_id": ObjectId("..."),
  "id": "0KmkdDrKlNG5GPuoF0sf3y",
  "nom": "Cumbia Classics",
  "genre": "latin",
  "subgenre": "cumbia",
  "tracks_count": 3,
  "tracks": [
    {
      "id": "1Y372uxsCkKqNclj2ercap",
      "name": "17 Años",
      "duration_ms": 181307,
      "duration_formatted": "03:01",
      "popularity": 68,
      "album": {
        "id": "3cwMyqMeTxBd26z6AjKGdv",
        "name": "Una Lluvia De Rosas",
        "release_date": "1999-01-01"
      },
      "artist": {
        "name": "los ángeles azules"
      },
      "audio_features": {
        "energy": 0.483,
        "tempo": 90.941,
        "danceability": 0.738,
        "loudness": -9.097,
        "valence": 0.774
      }
    }
  ],
  "_metadata": {
    "generated_at": "2025-12-04T...",
    "source": "spotify_xml_export"
  }
}
```

**Avantages de MongoDB** :
- Structure hiérarchique naturelle (playlists → tracks)
- Requêtes flexibles sur les tracks imbriqués
- Agrégations puissantes pour l'analyse
- Pas de jointures nécessaires

## Dépannage

### Pipeline 1 (Oracle)

#### Erreur de connexion Oracle

- Vérifiez que Oracle Database est démarré
- Vérifiez les identifiants dans `config.py` ou les variables d'environnement
- Testez avec : `python main.py --test-connection`

#### Erreur "ORA-12154: TNS"

- Vérifiez le format du DSN : `host:port/service_name`
- Exemple : `localhost:1521/XEPDB1`

#### Tables déjà existantes

- Utilisez `--full-reset` pour supprimer et recréer les tables

#### Fichier CSV introuvable

- Vérifiez que `data/input/high_popularity_spotify_data.csv` existe
- Vérifiez les permissions de lecture

### Pipeline 2 (MongoDB)

#### Erreur de connexion MongoDB

- Vérifiez que MongoDB est démarré : `mongod --version`
- Sous Windows, vérifiez le service : `services.msc` → MongoDB Server
- Sous Linux/Mac : `sudo systemctl status mongod`
- Testez avec : `python main.py --test-mongodb`

#### Erreur "ServerSelectionTimeoutError"

- MongoDB n'est pas accessible sur le port spécifié
- Vérifiez que MongoDB écoute sur `localhost:27017` (port par défaut)
- Vérifiez les paramètres dans `config.py` : `MONGO_HOST` et `MONGO_PORT`

#### Fichier XML introuvable

- Le pipeline MongoDB nécessite que le fichier XML existe
- Exécutez d'abord : `python main.py --full-reset`
- Le fichier doit être à : `data/output/spotify_data_export.xml`

#### Erreur de validation XSD

- Le XML doit être conforme au schéma XSD
- Vérifiez les logs de validation pour identifier les erreurs
- Le XSD est généré automatiquement, ne le modifiez pas manuellement

#### ModuleNotFoundError: pymongo

- Installez la dépendance : `pip install pymongo`
- Ou installez toutes les dépendances : `pip install -r requirements.txt`

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

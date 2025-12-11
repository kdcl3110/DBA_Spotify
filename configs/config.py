# Fichier : config.py

import os

# --- Configuration de la Base de Données Oracle ---
DB_USER = os.environ.get("DB_USER", "spotify_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "spotify123")
DB_DSN = os.environ.get("DB_DSN", "localhost:1521/XEPDB1")

# --- Configuration MongoDB ---
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "27017"))
MONGO_DATABASE = os.environ.get("MONGO_DATABASE", "spotify_db")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "playlists")

# --- Fichier de Données ---
CSV_FILE_PATH = "./data/input/high_popularity_spotify_data.csv"
XML_OUTPUT_PATH = "./data/output/spotify_data_export.xml"

# --- Fichiers DTD ---
DTD_PATH = "./data/output/spotify_data.dtd"
DTD_DOCUMENTATION_PATH = "./data/output/test_DTD_DOCUMENTATION.txt"

# --- Fichiers XSD ---
XSD_PATH = "./data/output/spotify_data.xsd"
XSD_DOCUMENTATION_PATH = "./data/output/XSD_DOCUMENTATION.txt"

# --- Fichiers XSLT et HTML ---
XSLT_FILE_PATH = "./data/input/spotify_transform.xslt"
HTML_OUTPUT_PATH = "./data/output/spotify_data.html"

# --- Fichiers XSLT pour JSON et JSON de sortie ---
XSLT_JSON_PATH = "./data/input/spotify_to_json.xslt"
JSON_OUTPUT_PATH = "./data/output/spotify_data.json"
# Fichier : config.py

import os

# --- Configuration de la Base de Données Oracle ---
DB_USER = os.environ.get("DB_USER", "spotify_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "spotify123") 
DB_DSN = os.environ.get("DB_DSN", "localhost:1521/XEPDB1")

# --- Fichier de Données ---
CSV_FILE_PATH = "./data/input/high_popularity_spotify_data.csv"
XML_OUTPUT_PATH = "./data/output/spotify_data_export.xml"
DTD_PATH = "./data/output/spotify_data.dtd"
DTD_DOCUMENTATION_PATH = "./data/output/test_DTD_DOCUMENTATION.txt"

# --- Fichiers XSLT et HTML ---
XSLT_FILE_PATH = "./data/input/spotify_transform.xslt"
HTML_OUTPUT_PATH = "./data/output/spotify_data.html"


# $env:DB_USER="spotify_prod_user"
# $env:DB_PASSWORD="MonMotDePasseSuperSecurise123"
# $env:DB_DSN="votre_serveur_oracle:1521/pdb1"

# # Vérifiez que c'est bien défini (facultatif)
# echo $env:DB_USER
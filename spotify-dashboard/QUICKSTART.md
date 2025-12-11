# Guide de Démarrage Rapide

## Installation en 2 étapes

### Étape 1: Installation des dépendances

Double-cliquez sur `install-all.bat` ou exécutez:

```bash
./install-all.bat
```

Cela installera automatiquement toutes les dépendances Node.js pour le backend et le frontend.

### Étape 2: Lancement du dashboard

Double-cliquez sur `start-dashboard.bat` ou exécutez:

```bash
./start-dashboard.bat
```

Cela va:
1. Démarrer MongoDB (si ce n'est pas déjà fait)
2. Lancer le serveur backend sur http://localhost:5000
3. Lancer le frontend sur http://localhost:3000

## Accès au Dashboard

Une fois lancé, ouvrez votre navigateur et allez sur:

**http://localhost:3000**

## Prérequis

Assurez-vous d'avoir:
- ✅ Node.js installé (version 16+)
- ✅ MongoDB installé et configuré
- ✅ Les données Spotify insérées dans MongoDB (via `python main.py --mongodb-pipeline`)

## Vérifier les données MongoDB

Avant de lancer le dashboard, vérifiez que vous avez des données:

```bash
mongosh
use spotify_db
db.playlists.countDocuments()
```

Si le résultat est 0, vous devez d'abord insérer les données:

```bash
# Retournez au dossier racine du projet
cd ..

# Exécutez le pipeline MongoDB
python main.py --mongodb-pipeline
```

## Problèmes courants

### MongoDB ne démarre pas

**Windows:**
```bash
net start MongoDB
```

**Linux/Mac:**
```bash
sudo systemctl start mongod
```

### Port déjà utilisé

Si le port 5000 ou 3000 est déjà utilisé, modifiez:
- Backend: `backend/.env` → changez `PORT=5000`
- Frontend: `frontend/vite.config.js` → changez `port: 3000`

### Erreur "Cannot find module"

Réinstallez les dépendances:

```bash
cd backend
npm install

cd ../frontend
npm install
```

## Arrêter le dashboard

Fermez simplement les fenêtres de terminal ouvertes par le script.

Ou utilisez Ctrl+C dans chaque terminal.

## Mode développement manuel

Si vous préférez lancer manuellement:

### Terminal 1 - Backend
```bash
cd spotify-dashboard/backend
npm start
```

### Terminal 2 - Frontend
```bash
cd spotify-dashboard/frontend
npm run dev
```

## Fonctionnalités du Dashboard

Une fois lancé, vous pouvez:

1. **Visualiser les statistiques globales** en haut de la page
2. **Filtrer par genre et sous-genre** avec le panneau de gauche
3. **Observer les graphiques**:
   - Distribution des genres (camembert)
   - Caractéristiques audio (barres)
4. **Trier les top tracks** par popularité, energy ou danceability
5. **Parcourir toutes les playlists** dans la grille en bas

## Design

Le dashboard utilise **Ant Design** pour un look moderne et professionnel:
- 💜 Dégradé principal Bleu-Violet (#667eea → #764ba2)
- 🎨 Design cards avec ombres douces et coins arrondis
- ✨ Animations au survol et effets de transparence
- 🎯 Header sticky transparent avec effet de blur
- 📊 Graphiques interactifs (Pie Chart, Radar Chart)
- 🏷️ Badges et Tags colorés pour les catégories
- 🎭 Icônes Ant Design pour une cohérence parfaite

## Pour aller plus loin

Consultez le fichier `README.md` pour:
- Documentation complète de l'API
- Guide de personnalisation
- Structure détaillée du projet
- Instructions de build de production

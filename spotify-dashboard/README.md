# Spotify Analytics Dashboard

Un dashboard moderne et interactif pour visualiser les données Spotify stockées dans MongoDB.

## Technologies

- **Frontend**: React 18 + Vite
- **UI Library**: Ant Design 5
- **Styling**: Tailwind CSS + Custom CSS
- **Charts**: Recharts
- **Icons**: Ant Design Icons
- **Backend**: Node.js + Express
- **Database**: MongoDB

## Design

Design moderne et professionnel avec Ant Design:
- **Layout**: Header sticky transparent avec effet de blur, cards avec ombres douces
- **Palette de couleurs**:
  - Dégradé principal: Bleu-Violet (#667eea → #764ba2)
  - Dégradés accentués: Rose (#f093fb → #f5576c), Cyan (#4facfe → #00f2fe)
- **Composants**: Cards arrondis, animations au survol, badges colorés
- **Background**: Dégradé violet en fond avec overlay transparent
- **Icons**: Ant Design Icons pour une cohérence visuelle parfaite

## Fonctionnalités

### Statistiques Globales
- Nombre total de playlists
- Nombre total de tracks
- Moyenne de tracks par playlist

### Filtres Dynamiques
- Filtrage par genre
- Filtrage par sous-genre (dépendant du genre sélectionné)
- Reset des filtres

### Visualisations
- **Distribution des genres**: Graphique en camembert
- **Caractéristiques audio**: Graphique en barres (energy, danceability, valence)
- **Top tracks**: Liste triable par popularité, energy ou danceability
- **Grille de playlists**: Affichage des playlists avec leurs informations

### API Endpoints

Backend REST API avec les endpoints suivants:
- `GET /api/stats` - Statistiques globales
- `GET /api/playlists` - Liste des playlists (avec filtres)
- `GET /api/playlists/:id` - Détails d'une playlist
- `GET /api/genres` - Liste des genres
- `GET /api/subgenres` - Liste des sous-genres
- `GET /api/tracks` - Top tracks (avec tri)
- `GET /api/audio-features` - Statistiques des caractéristiques audio

## Installation

### Prérequis

- Node.js 16+ et npm
- MongoDB installé et en cours d'exécution
- Les données Spotify déjà insérées dans MongoDB (via le pipeline principal)

### 1. Installation du Backend

```bash
cd spotify-dashboard/backend
npm install
```

### 2. Configuration du Backend

Modifiez le fichier `.env` si nécessaire:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=spotify_db
```

### 3. Installation du Frontend

```bash
cd spotify-dashboard/frontend
npm install
```

## Lancement

### 1. Démarrer MongoDB

Assurez-vous que MongoDB est en cours d'exécution:

```bash
# Windows
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
```

### 2. Démarrer le Backend

```bash
cd spotify-dashboard/backend
npm start
```

Le serveur démarre sur `http://localhost:5000`

### 3. Démarrer le Frontend

Dans un nouveau terminal:

```bash
cd spotify-dashboard/frontend
npm run dev
```

Le dashboard sera accessible sur `http://localhost:3000`

## Utilisation

1. **Vue d'ensemble**: Les statistiques globales s'affichent en haut
2. **Filtres**: Utilisez le panneau de filtres à gauche pour filtrer par genre/sous-genre
3. **Visualisations**: Observez les graphiques qui se mettent à jour en temps réel
4. **Top Tracks**: Changez le tri pour voir les tracks par différents critères
5. **Playlists**: Parcourez toutes les playlists filtrées

## Structure du Projet

```
spotify-dashboard/
├── backend/
│   ├── server.js           # API Express
│   ├── package.json
│   └── .env                # Configuration
└── frontend/
    ├── src/
    │   ├── components/     # Composants React
    │   │   ├── StatCard.jsx
    │   │   ├── FilterPanel.jsx
    │   │   ├── GenreChart.jsx
    │   │   ├── AudioFeaturesChart.jsx
    │   │   ├── TopTracks.jsx
    │   │   └── PlaylistsGrid.jsx
    │   ├── services/
    │   │   └── api.js      # Client API
    │   ├── App.jsx         # Composant principal
    │   ├── main.jsx
    │   └── index.css       # Styles Tailwind
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

## Personnalisation

### Modifier les couleurs

Éditez `frontend/tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      primary: { ... },  // Modifier la couleur primaire
      accent: { ... },   // Modifier la couleur accent
      success: { ... },  // Modifier la couleur succès
    }
  }
}
```

### Ajouter de nouveaux graphiques

1. Créez un nouveau composant dans `frontend/src/components/`
2. Importez-le dans `App.jsx`
3. Ajoutez-le à la grille de visualisation

## Dépannage

### Erreur de connexion MongoDB

- Vérifiez que MongoDB est démarré
- Vérifiez l'URI dans `.env`
- Testez avec: `mongo` ou `mongosh`

### Erreur CORS

- Le backend est configuré pour accepter toutes les origines
- Vérifiez que le backend tourne sur le bon port

### Pas de données affichées

- Vérifiez que les données sont bien dans MongoDB:
  ```bash
  mongosh
  use spotify_db
  db.playlists.count()
  ```
- Exécutez le pipeline MongoDB principal si nécessaire

## Développement

### Mode développement avec hot-reload

Backend:
```bash
cd backend
npm install -D nodemon
npm run dev
```

Frontend:
```bash
cd frontend
npm run dev
```

### Build de production

```bash
cd frontend
npm run build
```

Les fichiers de production seront dans `frontend/dist/`

## Licence

MIT

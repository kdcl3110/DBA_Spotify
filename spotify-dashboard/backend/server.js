import express from 'express';
import cors from 'cors';
import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const MONGODB_DATABASE = process.env.MONGODB_DATABASE || 'spotify_db';

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB Client
let db;
const client = new MongoClient(MONGODB_URI);

// Connect to MongoDB
async function connectDB() {
  try {
    await client.connect();
    db = client.db(MONGODB_DATABASE);
    console.log(`✅ Connected to MongoDB: ${MONGODB_DATABASE}`);
  } catch (error) {
    console.error('❌ MongoDB connection error:', error);
    process.exit(1);
  }
}

// Routes

// GET /api/stats - Global statistics
app.get('/api/stats', async (req, res) => {
  try {
    const playlists = db.collection('playlists');

    // Count total playlists
    const totalPlaylists = await playlists.countDocuments();

    // Get all playlists to calculate stats
    const allPlaylists = await playlists.find({}).toArray();

    // Calculate total tracks
    const totalTracks = allPlaylists.reduce((sum, p) => sum + (p.tracks?.length || 0), 0);

    // Calculate average tracks per playlist
    const avgTracksPerPlaylist = totalPlaylists > 0 ? totalTracks / totalPlaylists : 0;

    // Genre distribution
    const genreDistribution = {};
    allPlaylists.forEach(p => {
      const genre = p.genre || 'Unknown';
      genreDistribution[genre] = (genreDistribution[genre] || 0) + 1;
    });

    // Average audio features
    let totalEnergy = 0, totalDanceability = 0, totalValence = 0;
    let trackCount = 0;

    allPlaylists.forEach(playlist => {
      playlist.tracks?.forEach(track => {
        if (track.audio_features) {
          totalEnergy += track.audio_features.energy || 0;
          totalDanceability += track.audio_features.danceability || 0;
          totalValence += track.audio_features.valence || 0;
          trackCount++;
        }
      });
    });

    const avgAudioFeatures = trackCount > 0 ? {
      energy: (totalEnergy / trackCount).toFixed(3),
      danceability: (totalDanceability / trackCount).toFixed(3),
      valence: (totalValence / trackCount).toFixed(3)
    } : null;

    res.json({
      totalPlaylists,
      totalTracks,
      avgTracksPerPlaylist: avgTracksPerPlaylist.toFixed(2),
      genreDistribution,
      avgAudioFeatures
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/playlists - Get all playlists with optional filters
app.get('/api/playlists', async (req, res) => {
  try {
    const { genre, subgenre, limit = 100, offset = 0 } = req.query;

    const filter = {};
    if (genre) filter.genre = genre;
    if (subgenre) filter.subgenre = subgenre;

    const playlists = await db.collection('playlists')
      .find(filter)
      .skip(parseInt(offset))
      .limit(parseInt(limit))
      .toArray();

    res.json(playlists);
  } catch (error) {
    console.error('Error fetching playlists:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/playlists/:id - Get single playlist by ID
app.get('/api/playlists/:id', async (req, res) => {
  try {
    const playlist = await db.collection('playlists')
      .findOne({ id: req.params.id });

    if (!playlist) {
      return res.status(404).json({ error: 'Playlist not found' });
    }

    res.json(playlist);
  } catch (error) {
    console.error('Error fetching playlist:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/genres - Get list of all genres
app.get('/api/genres', async (req, res) => {
  try {
    const genres = await db.collection('playlists').distinct('genre');
    res.json(genres.filter(g => g)); // Remove null/undefined
  } catch (error) {
    console.error('Error fetching genres:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/subgenres - Get list of all subgenres (optionally filtered by genre)
app.get('/api/subgenres', async (req, res) => {
  try {
    const { genre } = req.query;
    const filter = genre ? { genre } : {};

    const subgenres = await db.collection('playlists').distinct('subgenre', filter);
    res.json(subgenres.filter(s => s)); // Remove null/undefined
  } catch (error) {
    console.error('Error fetching subgenres:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/tracks - Get top tracks with optional sorting
app.get('/api/tracks', async (req, res) => {
  try {
    const { sortBy = 'popularity', limit = 20 } = req.query;

    const playlists = await db.collection('playlists').find({}).toArray();

    // Extract all tracks from all playlists
    const allTracks = [];
    playlists.forEach(playlist => {
      playlist.tracks?.forEach(track => {
        allTracks.push({
          ...track,
          playlistName: playlist.nom,
          playlistGenre: playlist.genre
        });
      });
    });

    // Sort tracks
    const sortField = sortBy === 'popularity' ? 'popularity' :
                      sortBy === 'energy' ? 'audio_features.energy' :
                      sortBy === 'danceability' ? 'audio_features.danceability' : 'popularity';

    allTracks.sort((a, b) => {
      const aVal = sortBy === 'popularity' ? a.popularity :
                   sortBy === 'energy' ? a.audio_features?.energy :
                   sortBy === 'danceability' ? a.audio_features?.danceability : 0;
      const bVal = sortBy === 'popularity' ? b.popularity :
                   sortBy === 'energy' ? b.audio_features?.energy :
                   sortBy === 'danceability' ? b.audio_features?.danceability : 0;
      return (bVal || 0) - (aVal || 0);
    });

    res.json(allTracks.slice(0, parseInt(limit)));
  } catch (error) {
    console.error('Error fetching tracks:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/audio-features - Get audio features statistics
app.get('/api/audio-features', async (req, res) => {
  try {
    const { genre, subgenre } = req.query;

    const filter = {};
    if (genre) filter.genre = genre;
    if (subgenre) filter.subgenre = subgenre;

    const playlists = await db.collection('playlists').find(filter).toArray();

    const features = {
      energy: [],
      danceability: [],
      valence: [],
      tempo: [],
      loudness: []
    };

    playlists.forEach(playlist => {
      playlist.tracks?.forEach(track => {
        if (track.audio_features) {
          const af = track.audio_features;
          if (af.energy !== undefined) features.energy.push(af.energy);
          if (af.danceability !== undefined) features.danceability.push(af.danceability);
          if (af.valence !== undefined) features.valence.push(af.valence);
          if (af.tempo !== undefined) features.tempo.push(af.tempo);
          if (af.loudness !== undefined) features.loudness.push(af.loudness);
        }
      });
    });

    // Calculate averages and distribution
    const stats = {};
    for (const [key, values] of Object.entries(features)) {
      if (values.length > 0) {
        const avg = values.reduce((a, b) => a + b, 0) / values.length;
        const min = Math.min(...values);
        const max = Math.max(...values);

        stats[key] = {
          avg: parseFloat(avg.toFixed(3)),
          min: parseFloat(min.toFixed(3)),
          max: parseFloat(max.toFixed(3)),
          count: values.length
        };
      }
    }

    res.json(stats);
  } catch (error) {
    console.error('Error fetching audio features:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

// Start server
connectDB().then(() => {
  app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
  });
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n⏹️  Shutting down gracefully...');
  await client.close();
  process.exit(0);
});

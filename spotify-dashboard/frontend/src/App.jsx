import React, { useState, useEffect } from 'react';
import { ConfigProvider, Layout, theme, Spin, Alert } from 'antd';
import StatCard from './components/StatCard';
import FilterPanel from './components/FilterPanel';
import GenreChart from './components/GenreChart';
import AudioFeaturesChart from './components/AudioFeaturesChart';
import TopTracks from './components/TopTracks';
import PlaylistsGrid from './components/PlaylistsGrid';
import { getStats, getPlaylists, getTracks, getAudioFeatures } from './services/api';

const { Header, Content } = Layout;

function App() {
  const [stats, setStats] = useState(null);
  const [playlists, setPlaylists] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [audioFeatures, setAudioFeatures] = useState(null);
  const [filters, setFilters] = useState({ genre: null, subgenre: null });
  const [trackSort, setTrackSort] = useState('popularity');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load global stats (unfiltered)
  useEffect(() => {
    loadStats();
  }, []);

  // Load filtered data when filters change
  useEffect(() => {
    loadFilteredData();
  }, [filters]);

  // Load tracks when sort changes
  useEffect(() => {
    loadTracks(trackSort);
  }, [trackSort]);

  const loadStats = async () => {
    try {
      const data = await getStats();
      setStats(data);
    } catch (err) {
      console.error('Error loading stats:', err);
      setError('Failed to load statistics');
    }
  };

  const loadFilteredData = async () => {
    setLoading(true);
    try {
      const filterParams = {};
      if (filters.genre) filterParams.genre = filters.genre;
      if (filters.subgenre) filterParams.subgenre = filters.subgenre;

      const [playlistsData, audioFeaturesData] = await Promise.all([
        getPlaylists(filterParams),
        getAudioFeatures(filterParams),
      ]);

      setPlaylists(playlistsData);
      setAudioFeatures(audioFeaturesData);
      setLoading(false);
    } catch (err) {
      console.error('Error loading filtered data:', err);
      setError('Failed to load data');
      setLoading(false);
    }
  };

  const loadTracks = async (sortBy) => {
    try {
      const data = await getTracks(sortBy, 20);
      setTracks(data);
    } catch (err) {
      console.error('Error loading tracks:', err);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleTrackSortChange = (sortBy) => {
    setTrackSort(sortBy);
  };

  if (error) {
    return (
      <ConfigProvider
        theme={{
          algorithm: theme.defaultAlgorithm,
          token: {
            colorPrimary: '#7C3AED',
            borderRadius: 8,
            fontFamily: 'Inter, sans-serif',
          },
        }}
      >
        <Layout style={{ minHeight: '100vh', background: 'transparent' }}>
          <Content style={{ padding: '50px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Alert
              message="Error"
              description={error}
              type="error"
              showIcon
              style={{ maxWidth: 500 }}
            />
          </Content>
        </Layout>
      </ConfigProvider>
    );
  }

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#7C3AED',
          borderRadius: 8,
          fontFamily: 'Inter, sans-serif',
        },
      }}
    >
      <Layout style={{ minHeight: '100vh', background: 'transparent' }}>
        {/* Header */}
        <Header
          style={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            padding: '0 50px',
            display: 'flex',
            alignItems: 'center',
            position: 'sticky',
            top: 0,
            zIndex: 100,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
            <div style={{
              fontSize: '28px',
              fontWeight: '700',
              color: '#1a1a1a',
              marginRight: '20px',
              letterSpacing: '-0.5px'
            }}>
              🎵 Spotify Analytics
            </div>
            <div style={{
              fontSize: '14px',
              color: '#666',
              marginTop: '5px'
            }}>
              Real-time data visualization dashboard
            </div>
          </div>
        </Header>

        {/* Main Content */}
        <Content style={{ padding: '30px 50px' }}>
          <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
            {/* Global Stats */}
            {stats && (
              <div style={{ marginBottom: '30px' }}>
                <StatCard stats={stats} />
              </div>
            )}

            {/* Main Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '24px', marginBottom: '30px' }}>
              {/* Filters Sidebar */}
              <div>
                <FilterPanel filters={filters} onFilterChange={handleFilterChange} />
              </div>

              {/* Charts and Data */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {/* Charts Row */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
                  {stats && <GenreChart data={stats.genreDistribution} />}
                  <AudioFeaturesChart data={audioFeatures} />
                </div>

                {/* Top Tracks */}
                <TopTracks tracks={tracks} onSortChange={handleTrackSortChange} />
              </div>
            </div>

            {/* Playlists Grid */}
            {loading ? (
              <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                padding: '100px',
                background: 'white',
                borderRadius: '12px'
              }}>
                <Spin size="large" tip="Loading playlists..." />
              </div>
            ) : (
              <PlaylistsGrid playlists={playlists} />
            )}
          </div>
        </Content>

        {/* Footer */}
        <div style={{
          textAlign: 'center',
          padding: '24px',
          color: 'white',
          fontSize: '14px',
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ fontWeight: '500' }}>
            Spotify Analytics Dashboard
          </div>
          <div style={{ fontSize: '12px', marginTop: '4px', opacity: 0.8 }}>
            Built with React, Ant Design, and MongoDB
          </div>
        </div>
      </Layout>
    </ConfigProvider>
  );
}

export default App;

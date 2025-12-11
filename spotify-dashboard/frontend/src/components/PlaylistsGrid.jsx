import React, { useState } from 'react';
import { Card, Row, Col, Tag, Empty, Badge, Modal, List, Avatar } from 'antd';
import { AppstoreOutlined, PlayCircleOutlined, SoundOutlined, UserOutlined, ClockCircleOutlined } from '@ant-design/icons';

const PlaylistsGrid = ({ playlists }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = useState(null);

  const handlePlaylistClick = (playlist) => {
    setSelectedPlaylist(playlist);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedPlaylist(null);
  };

  if (!playlists || playlists.length === 0) {
    return (
      <Card
        title={
          <span style={{ fontSize: '16px', fontWeight: '600' }}>
            <AppstoreOutlined style={{ marginRight: '8px' }} />
            Playlists
          </span>
        }
        bordered={false}
        style={{ borderRadius: '12px' }}
      >
        <Empty description="No playlists found" />
      </Card>
    );
  }

  const getGenreColor = (genre) => {
    const colors = {
      latin: { bg: '#FEF3C7', color: '#CA8A04', border: '#FCD34D' },
      pop: { bg: '#FCE7F3', color: '#DB2777', border: '#F9A8D4' },
      rock: { bg: '#FEE2E2', color: '#DC2626', border: '#FECACA' },
      jazz: { bg: '#FAF5FF', color: '#7C3AED', border: '#E9D5FF' },
      classical: { bg: '#EFF6FF', color: '#2563EB', border: '#BFDBFE' },
      electronic: { bg: '#F0FDFA', color: '#0D9488', border: '#99F6E4' },
      rnb: { bg: '#FFF7ED', color: '#EA580C', border: '#FED7AA' },
      hiphop: { bg: '#F3F4F6', color: '#4B5563', border: '#D1D5DB' },
    };
    return colors[genre?.toLowerCase()] || { bg: '#F9FAFB', color: '#6B7280', border: '#E5E7EB' };
  };

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: '600' }}>
          <AppstoreOutlined style={{ marginRight: '8px' }} />
          Playlists
          <Badge
            count={playlists.length}
            style={{
              backgroundColor: '#7C3AED',
              marginLeft: '12px',
            }}
          />
        </span>
      }
      bordered={false}
      style={{ borderRadius: '12px' }}
    >
      <Row gutter={[16, 16]}>
        {playlists.map((playlist) => {
          const genreStyle = getGenreColor(playlist.genre);

          return (
            <Col xs={24} sm={12} md={8} lg={6} key={playlist.id}>
              <Card
                hoverable
                bordered={false}
                onClick={() => handlePlaylistClick(playlist)}
                style={{
                  borderRadius: '12px',
                  background: 'white',
                  border: '1px solid #e8e8e8',
                  height: '100%',
                  cursor: 'pointer',
                }}
                bodyStyle={{ padding: '16px' }}
              >
                <div style={{ marginBottom: '12px' }}>
                  <div
                    style={{
                      fontSize: '16px',
                      fontWeight: '600',
                      color: '#333',
                      marginBottom: '8px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                    title={playlist.nom}
                  >
                    <PlayCircleOutlined style={{ marginRight: '6px', color: genreStyle.color }} />
                    {playlist.nom}
                  </div>
                </div>

                <div style={{ marginBottom: '12px' }}>
                  <Tag
                    style={{
                      borderRadius: '6px',
                      fontSize: '12px',
                      marginBottom: '4px',
                      background: genreStyle.bg,
                      color: genreStyle.color,
                      border: `1px solid ${genreStyle.border}`,
                    }}
                  >
                    {playlist.genre}
                  </Tag>
                  {playlist.subgenre && (
                    <Tag
                      style={{
                        borderRadius: '6px',
                        fontSize: '12px',
                        background: '#f0f0f0',
                        color: '#666',
                        border: '1px solid #E8E8E8',
                      }}
                    >
                      {playlist.subgenre}
                    </Tag>
                  )}
                </div>

                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    paddingTop: '12px',
                    borderTop: '1px solid #e8e8e8',
                  }}
                >
                  <span style={{ fontSize: '13px', color: '#999' }}>
                    <SoundOutlined style={{ marginRight: '4px' }} />
                    {/* Tracks */}
                  </span>
                  <span
                    style={{
                      fontSize: '18px',
                      fontWeight: 'bold',
                      color: genreStyle.color,
                    }}
                  >
                    {playlist.tracks_count || playlist.tracks?.length || 0}
                  </span>
                </div>
              </Card>
            </Col>
          );
        })}
      </Row>

      {/* Modal for Playlist Tracks */}
      <Modal
        title={
          selectedPlaylist ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <PlayCircleOutlined style={{ fontSize: '24px', color: getGenreColor(selectedPlaylist.genre).color }} />
              <div>
                <div style={{ fontSize: '18px', fontWeight: '600' }}>{selectedPlaylist.nom}</div>
                <div style={{ fontSize: '13px', color: '#999', fontWeight: 'normal' }}>
                  {selectedPlaylist.tracks?.length || selectedPlaylist.tracks_count || 0} tracks
                </div>
              </div>
            </div>
          ) : 'Playlist Details'
        }
        open={isModalOpen}
        onCancel={handleCloseModal}
        footer={null}
        width={700}
        style={{ top: 20 }}
      >
        {selectedPlaylist && (
          <div>
            {/* Playlist Info */}
            <div style={{ marginBottom: '20px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <Tag
                style={{
                  borderRadius: '6px',
                  padding: '4px 12px',
                  background: getGenreColor(selectedPlaylist.genre).bg,
                  color: getGenreColor(selectedPlaylist.genre).color,
                  border: `1px solid ${getGenreColor(selectedPlaylist.genre).border}`,
                }}
              >
                {selectedPlaylist.genre}
              </Tag>
              {selectedPlaylist.subgenre && (
                <Tag
                  style={{
                    borderRadius: '6px',
                    padding: '4px 12px',
                    background: '#f0f0f0',
                    color: '#666',
                    border: '1px solid #E8E8E8',
                  }}
                >
                  {selectedPlaylist.subgenre}
                </Tag>
              )}
            </div>

            {/* Tracks List */}
            {selectedPlaylist.tracks && selectedPlaylist.tracks.length > 0 ? (
              <List
                dataSource={selectedPlaylist.tracks}
                style={{ maxHeight: '500px', overflowY: 'auto' }}
                renderItem={(track, index) => (
                  <List.Item
                    style={{
                      padding: '12px 16px',
                      borderRadius: '8px',
                      marginBottom: '8px',
                      background: index % 2 === 0 ? '#FAFAFA' : 'white',
                    }}
                  >
                    <List.Item.Meta
                      avatar={
                        <Avatar
                          style={{
                            background: getGenreColor(selectedPlaylist.genre).color,
                            color: 'white',
                            fontWeight: '600',
                          }}
                        >
                          {index + 1}
                        </Avatar>
                      }
                      title={
                        <div style={{ fontWeight: '500', fontSize: '14px', color: '#333' }}>
                          {track.name || track.titre || 'Unknown Track'}
                        </div>
                      }
                      description={
                        <div style={{ fontSize: '13px', color: '#666', display: 'flex', alignItems: 'center', gap: '12px' }}>
                          <span>
                            <UserOutlined style={{ marginRight: '4px' }} />
                            {track.artist?.name || track.artiste || 'Unknown Artist'}
                          </span>
                          {track.duration_ms && (
                            <span>
                              <ClockCircleOutlined style={{ marginRight: '4px' }} />
                              {Math.floor(track.duration_ms / 60000)}:{String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                            </span>
                          )}
                        </div>
                      }
                    />
                    {track.popularity !== undefined && (
                      <Tag
                        style={{
                          background: track.popularity >= 70 ? '#DC2626' : track.popularity >= 50 ? '#EA580C' : '#CA8A04',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          fontWeight: '600',
                        }}
                      >
                        {track.popularity}
                      </Tag>
                    )}
                  </List.Item>
                )}
              />
            ) : (
              <Empty description="No tracks available" />
            )}
          </div>
        )}
      </Modal>
    </Card>
  );
};

export default PlaylistsGrid;

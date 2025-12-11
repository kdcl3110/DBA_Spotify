import React from 'react';
import { Card, Row, Col, Tag, Empty, Badge } from 'antd';
import { AppstoreOutlined, PlayCircleOutlined, SoundOutlined } from '@ant-design/icons';

const PlaylistsGrid = ({ playlists }) => {
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
                style={{
                  borderRadius: '12px',
                  background: 'white',
                  border: '1px solid #e8e8e8',
                  height: '100%',
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
                    Tracks
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
    </Card>
  );
};

export default PlaylistsGrid;

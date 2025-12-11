import React, { useState } from 'react';
import { Card, List, Avatar, Tag, Select, Empty } from 'antd';
import { TrophyOutlined, FireOutlined, ThunderboltOutlined, SoundOutlined } from '@ant-design/icons';

const { Option } = Select;

const TopTracks = ({ tracks, onSortChange }) => {
  const [sortBy, setSortBy] = useState('popularity');

  const handleSortChange = (value) => {
    setSortBy(value);
    onSortChange(value);
  };

  if (!tracks || tracks.length === 0) {
    return (
      <Card
        title={
          <span style={{ fontSize: '16px', fontWeight: '600' }}>
            <TrophyOutlined style={{ marginRight: '8px' }} />
            Top Tracks
          </span>
        }
        bordered={false}
        style={{ borderRadius: '12px' }}
      >
        <Empty description="No tracks available" />
      </Card>
    );
  }

  const getSortIcon = () => {
    switch (sortBy) {
      case 'popularity':
        return <FireOutlined />;
      case 'energy':
        return <ThunderboltOutlined />;
      case 'danceability':
        return <SoundOutlined />;
      default:
        return <FireOutlined />;
    }
  };

  const getTagColor = (value, sortBy) => {
    if (sortBy === 'popularity') {
      return value >= 80 ? { bg: '#DC2626', color: 'white' } : value >= 60 ? { bg: '#EA580C', color: 'white' } : { bg: '#CA8A04', color: 'white' };
    } else {
      return value >= 70 ? { bg: '#7C3AED', color: 'white' } : value >= 50 ? { bg: '#2563EB', color: 'white' } : { bg: '#0D9488', color: 'white' };
    }
  };

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: '600' }}>
          <TrophyOutlined style={{ marginRight: '8px' }} />
          Top Tracks
        </span>
      }
      bordered={false}
      style={{ borderRadius: '12px' }}
      extra={
        <Select
          value={sortBy}
          onChange={handleSortChange}
          style={{ width: 180 }}
          suffixIcon={getSortIcon()}
        >
          <Option value="popularity">
            <FireOutlined /> By Popularity
          </Option>
          <Option value="energy">
            <ThunderboltOutlined /> By Energy
          </Option>
          <Option value="danceability">
            <SoundOutlined /> By Danceability
          </Option>
        </Select>
      }
    >
      <List
        itemLayout="horizontal"
        dataSource={tracks}
        style={{ maxHeight: '500px', overflowY: 'auto' }}
        renderItem={(track, index) => {
          let value, displayValue;

          if (sortBy === 'popularity') {
            value = track.popularity || 0;
            displayValue = value;
          } else if (sortBy === 'energy' && track.audio_features) {
            value = (track.audio_features.energy * 100);
            displayValue = `${value.toFixed(0)}%`;
          } else if (sortBy === 'danceability' && track.audio_features) {
            value = (track.audio_features.danceability * 100);
            displayValue = `${value.toFixed(0)}%`;
          } else {
            value = 0;
            displayValue = 'N/A';
          }

          const tagStyle = getTagColor(value, sortBy);

          const avatarColors = ['#DC2626', '#EA580C', '#CA8A04'];
          const avatarBg = index < 3 ? avatarColors[index] : '#E5E7EB';

          return (
            <List.Item
              style={{
                background: index < 3 ? '#FEF9F5' : 'transparent',
                padding: '12px 16px',
                borderRadius: '8px',
                marginBottom: '8px',
                border: index < 3 ? '1px solid #FDEDD3' : 'none',
              }}
            >
              <List.Item.Meta
                avatar={
                  <Avatar
                    style={{
                      background: avatarBg,
                      color: index < 3 ? 'white' : '#9CA3AF',
                      fontWeight: 'bold',
                      fontSize: '16px',
                    }}
                  >
                    {index + 1}
                  </Avatar>
                }
                title={
                  <span style={{ fontWeight: index < 3 ? '600' : '500', fontSize: '14px' }}>
                    {track.name}
                  </span>
                }
                description={
                  <span style={{ fontSize: '13px', color: '#666' }}>
                    {track.artist?.name || 'Unknown Artist'}
                  </span>
                }
              />
              <Tag
                style={{
                  fontSize: '14px',
                  padding: '4px 12px',
                  borderRadius: '8px',
                  fontWeight: '600',
                  background: tagStyle.bg,
                  color: tagStyle.color,
                  border: 'none',
                }}
              >
                {displayValue}
              </Tag>
            </List.Item>
          );
        }}
      />
    </Card>
  );
};

export default TopTracks;

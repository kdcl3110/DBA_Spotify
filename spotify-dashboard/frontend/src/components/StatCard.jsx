import React from 'react';
import { Card, Row, Col } from 'antd';
import {
  UnorderedListOutlined,
  CustomerServiceOutlined,
  BarChartOutlined
} from '@ant-design/icons';

const StatCard = ({ stats }) => {
  const statsData = [
    {
      title: 'Total Playlists',
      value: stats.totalPlaylists,
      icon: <UnorderedListOutlined style={{ fontSize: '32px' }} />,
      color: '#0D9488',
      bgColor: '#F0FDFA',
    },
    {
      title: 'Total Tracks',
      value: stats.totalTracks,
      icon: <CustomerServiceOutlined style={{ fontSize: '32px' }} />,
      color: '#EA580C',
      bgColor: '#FFF7ED',
    },
    {
      title: 'Avg Tracks/Playlist',
      value: stats.avgTracksPerPlaylist,
      precision: 2,
      icon: <BarChartOutlined style={{ fontSize: '32px' }} />,
      color: '#7C3AED',
      bgColor: '#FAF5FF',
    },
  ];

  return (
    <>
      {/* Main Stats Row */}
      <Row gutter={[24, 24]}>
        {statsData.map((stat, index) => (
          <Col xs={24} sm={12} lg={8} key={index}>
            <Card
              bordered={false}
              style={{
                background: stat.bgColor,
                borderRadius: '12px',
                overflow: 'hidden',
                border: '1px solid #E8E8E8',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ color: '#666', fontSize: '13px', marginBottom: '8px', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    {stat.title}
                  </div>
                  <div style={{ color: stat.color, fontSize: '32px', fontWeight: '700' }}>
                    {stat.value}
                  </div>
                </div>
                <div style={{
                  color: stat.color,
                  background: 'white',
                  padding: '16px',
                  borderRadius: '12px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
                }}>
                  {stat.icon}
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>
    </>
  );
};

export default StatCard;

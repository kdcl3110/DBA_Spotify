import React from 'react';
import { Card, Empty, Row, Col, Statistic } from 'antd';
import { ThunderboltOutlined } from '@ant-design/icons';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const AudioFeaturesChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <Card
        title={
          <span style={{ fontSize: '16px', fontWeight: '600' }}>
            <ThunderboltOutlined style={{ marginRight: '8px' }} />
            Audio Features Analysis
          </span>
        }
        bordered={false}
        style={{ borderRadius: '12px', height: '100%' }}
      >
        <Empty description="No data available" />
      </Card>
    );
  }

  // Prepare data for radar chart
  const radarData = Object.entries(data)
    .filter(([key]) => ['energy', 'danceability', 'valence'].includes(key))
    .map(([name, stats]) => ({
      feature: name.charAt(0).toUpperCase() + name.slice(1),
      value: parseFloat((stats.avg * 100).toFixed(1)),
    }));

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: '600' }}>
          <ThunderboltOutlined style={{ marginRight: '8px' }} />
          Audio Features Analysis
        </span>
      }
      bordered={false}
      style={{ borderRadius: '12px', height: '100%' }}
    >
      <ResponsiveContainer width="100%" height={200}>
        <RadarChart data={radarData}>
          <PolarGrid stroke="#e0e0e0" />
          <PolarAngleAxis
            dataKey="feature"
            tick={{ fill: '#666', fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: '#999', fontSize: 10 }}
          />
          <Radar
            name="Average %"
            dataKey="value"
            stroke="#7C3AED"
            fill="#7C3AED"
            fillOpacity={0.4}
          />
          <Tooltip
            contentStyle={{
              background: 'rgba(255, 255, 255, 0.95)',
              border: 'none',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            }}
          />
        </RadarChart>
      </ResponsiveContainer>

      <Row gutter={16} style={{ marginTop: '20px' }}>
        {data.tempo && (
          <Col span={12}>
            <div style={{
              background: '#EFF6FF',
              border: '1px solid #BFDBFE',
              borderRadius: '8px',
              padding: '16px',
              textAlign: 'center'
            }}>
              <div style={{ color: '#1E40AF', fontSize: '12px', marginBottom: '4px', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                Avg Tempo
              </div>
              <div style={{ color: '#2563EB', fontSize: '24px', fontWeight: '700' }}>
                {data.tempo.avg}
              </div>
              <div style={{ color: '#3B82F6', fontSize: '12px', fontWeight: '500' }}>
                BPM
              </div>
            </div>
          </Col>
        )}
        {data.loudness && (
          <Col span={12}>
            <div style={{
              background: '#FEF3C7',
              border: '1px solid #FCD34D',
              borderRadius: '8px',
              padding: '16px',
              textAlign: 'center'
            }}>
              <div style={{ color: '#92400E', fontSize: '12px', marginBottom: '4px', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                Avg Loudness
              </div>
              <div style={{ color: '#CA8A04', fontSize: '24px', fontWeight: '700' }}>
                {data.loudness.avg}
              </div>
              <div style={{ color: '#D97706', fontSize: '12px', fontWeight: '500' }}>
                dB
              </div>
            </div>
          </Col>
        )}
      </Row>
    </Card>
  );
};

export default AudioFeaturesChart;

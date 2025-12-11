import React from 'react';
import { Card, Empty } from 'antd';
import { PieChartOutlined } from '@ant-design/icons';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#0D9488', '#EA580C', '#7C3AED', '#DC2626', '#2563EB', '#CA8A04', '#DB2777', '#059669'];

const GenreChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <Card
        title={
          <span style={{ fontSize: '16px', fontWeight: '600' }}>
            <PieChartOutlined style={{ marginRight: '8px' }} />
            Genre Distribution
          </span>
        }
        bordered={false}
        style={{ borderRadius: '12px', height: '100%' }}
      >
        <Empty description="No data available" />
      </Card>
    );
  }

  const chartData = Object.entries(data).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
  }));

  const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        style={{ fontSize: '14px', fontWeight: 'bold', textShadow: '0 1px 3px rgba(0,0,0,0.3)' }}
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: '600' }}>
          <PieChartOutlined style={{ marginRight: '8px' }} />
          Genre Distribution
        </span>
      }
      bordered={false}
      style={{ borderRadius: '12px', height: '100%' }}
    >
      <ResponsiveContainer width="100%" height={320}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderLabel}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              background: 'rgba(255, 255, 255, 0.95)',
              border: 'none',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            }}
          />
          <Legend
            wrapperStyle={{
              paddingTop: '20px',
            }}
            iconType="circle"
          />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default GenreChart;

import React, { useEffect, useState } from 'react';
import { Card, Select, Button, Space, Tag, Divider, Spin } from 'antd';
import { FilterOutlined, ReloadOutlined } from '@ant-design/icons';
import { getGenres, getSubgenres } from '../services/api';

const { Option } = Select;

const FilterPanel = ({ filters, onFilterChange }) => {
  const [genres, setGenres] = useState([]);
  const [subgenres, setSubgenres] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGenres();
  }, []);

  useEffect(() => {
    if (filters.genre) {
      loadSubgenres(filters.genre);
    } else {
      setSubgenres([]);
    }
  }, [filters.genre]);

  const loadGenres = async () => {
    try {
      const data = await getGenres();
      setGenres(data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading genres:', error);
      setLoading(false);
    }
  };

  const loadSubgenres = async (genre) => {
    try {
      const data = await getSubgenres(genre);
      setSubgenres(data);
    } catch (error) {
      console.error('Error loading subgenres:', error);
    }
  };

  const handleGenreChange = (value) => {
    onFilterChange({ ...filters, genre: value || null, subgenre: null });
  };

  const handleSubgenreChange = (value) => {
    onFilterChange({ ...filters, subgenre: value || null });
  };

  const handleReset = () => {
    onFilterChange({ genre: null, subgenre: null });
  };

  if (loading) {
    return (
      <Card
        title={
          <span>
            <FilterOutlined /> Filters
          </span>
        }
        bordered={false}
        style={{ borderRadius: '12px' }}
      >
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin />
        </div>
      </Card>
    );
  }

  return (
    <Card
      title={
        <span style={{ fontSize: '16px', fontWeight: '600' }}>
          <FilterOutlined style={{ marginRight: '8px' }} />
          Filters
        </span>
      }
      bordered={false}
      style={{ borderRadius: '12px' }}
      extra={
        <Button
          type="text"
          size="small"
          icon={<ReloadOutlined />}
          onClick={handleReset}
          disabled={!filters.genre && !filters.subgenre}
        >
          Reset
        </Button>
      }
    >
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        {/* Genre Filter */}
        <div>
          <label style={{
            display: 'block',
            marginBottom: '8px',
            fontSize: '14px',
            fontWeight: '500',
            color: '#666'
          }}>
            Genre
          </label>
          <Select
            value={filters.genre}
            onChange={handleGenreChange}
            style={{ width: '100%' }}
            placeholder="Select a genre"
            allowClear
            size="large"
          >
            {genres.map((genre) => (
              <Option key={genre} value={genre}>
                {genre.charAt(0).toUpperCase() + genre.slice(1)}
              </Option>
            ))}
          </Select>
        </div>

        {/* Subgenre Filter */}
        {filters.genre && subgenres.length > 0 && (
          <div>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              fontSize: '14px',
              fontWeight: '500',
              color: '#666'
            }}>
              Subgenre
            </label>
            <Select
              value={filters.subgenre}
              onChange={handleSubgenreChange}
              style={{ width: '100%' }}
              placeholder="Select a subgenre"
              allowClear
              size="large"
            >
              {subgenres.map((subgenre) => (
                <Option key={subgenre} value={subgenre}>
                  {subgenre.charAt(0).toUpperCase() + subgenre.slice(1)}
                </Option>
              ))}
            </Select>
          </div>
        )}

        {/* Active Filters */}
        {(filters.genre || filters.subgenre) && (
          <>
            <Divider style={{ margin: '8px 0' }} />
            <div>
              <div style={{
                fontSize: '12px',
                fontWeight: '500',
                color: '#999',
                marginBottom: '8px',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Active Filters
              </div>
              <Space size={[0, 8]} wrap>
                {filters.genre && (
                  <Tag
                    color="default"
                    closable
                    onClose={() => handleGenreChange(null)}
                    style={{
                      borderRadius: '6px',
                      padding: '4px 12px',
                      background: '#F0FDFA',
                      border: '1px solid #0D9488',
                      color: '#0D9488',
                    }}
                  >
                    Genre: {filters.genre}
                  </Tag>
                )}
                {filters.subgenre && (
                  <Tag
                    color="default"
                    closable
                    onClose={() => handleSubgenreChange(null)}
                    style={{
                      borderRadius: '6px',
                      padding: '4px 12px',
                      background: '#FAF5FF',
                      border: '1px solid #7C3AED',
                      color: '#7C3AED',
                    }}
                  >
                    Subgenre: {filters.subgenre}
                  </Tag>
                )}
              </Space>
            </div>
          </>
        )}
      </Space>
    </Card>
  );
};

export default FilterPanel;

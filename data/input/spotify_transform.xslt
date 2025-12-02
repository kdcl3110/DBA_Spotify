<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>

    <!-- Template principal -->
    <xsl:template match="/">
        <html lang="fr">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Spotify Analytics Dashboard</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap');

                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }

                    body {
                        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        background: #0a0e27;
                        color: #e4e6eb;
                        min-height: 100vh;
                    }

                    .dashboard-container {
                        display: grid;
                        grid-template-columns: 280px 1fr;
                        min-height: 100vh;
                    }

                    /* Sidebar */
                    .sidebar {
                        background: linear-gradient(180deg, #141b2d 0%, #0f1419 100%);
                        border-right: 1px solid #1e293b;
                        padding: 30px 20px;
                        position: sticky;
                        top: 0;
                        height: 100vh;
                        overflow-y: auto;
                    }

                    .logo {
                        display: flex;
                        align-items: center;
                        gap: 12px;
                        margin-bottom: 40px;
                        padding-bottom: 25px;
                        border-bottom: 1px solid #1e293b;
                    }

                    .logo-icon {
                        width: 40px;
                        height: 40px;
                        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                    }

                    .logo-text {
                        font-size: 18px;
                        font-weight: 700;
                        color: #fff;
                    }

                    .sidebar-stats {
                        display: flex;
                        flex-direction: column;
                        gap: 15px;
                    }

                    .sidebar-stat {
                        background: rgba(30, 41, 59, 0.5);
                        padding: 18px;
                        border-radius: 12px;
                        border: 1px solid #1e293b;
                    }

                    .sidebar-stat-label {
                        font-size: 11px;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                        color: #64748b;
                        margin-bottom: 8px;
                        font-weight: 600;
                    }

                    .sidebar-stat-value {
                        font-size: 28px;
                        font-weight: 700;
                        color: #fff;
                    }

                    .sidebar-stat-sublabel {
                        font-size: 12px;
                        color: #94a3b8;
                        margin-top: 4px;
                    }

                    /* Main Content */
                    .main-content {
                        padding: 40px;
                        background: #0a0e27;
                        overflow-y: auto;
                    }

                    .page-header {
                        margin-bottom: 35px;
                    }

                    .page-title {
                        font-size: 32px;
                        font-weight: 700;
                        color: #fff;
                        margin-bottom: 8px;
                    }

                    .page-subtitle {
                        font-size: 14px;
                        color: #94a3b8;
                    }

                    /* Charts Section */
                    .charts-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                        gap: 25px;
                        margin-bottom: 35px;
                    }

                    .chart-card {
                        background: linear-gradient(135deg, #141b2d 0%, #1a2332 100%);
                        border: 1px solid #1e293b;
                        border-radius: 16px;
                        padding: 25px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                    }

                    .chart-card-title {
                        font-size: 16px;
                        font-weight: 600;
                        color: #fff;
                        margin-bottom: 20px;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }

                    .chart-card-title-icon {
                        width: 8px;
                        height: 8px;
                        background: #1DB954;
                        border-radius: 50%;
                    }

                    .chart-container {
                        position: relative;
                        height: 280px;
                    }

                    /* Playlists Section */
                    .playlists-section {
                        margin-top: 40px;
                    }

                    .section-title {
                        font-size: 20px;
                        font-weight: 700;
                        color: #fff;
                        margin-bottom: 20px;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    }

                    .playlist-card {
                        background: linear-gradient(135deg, #141b2d 0%, #1a2332 100%);
                        border: 1px solid #1e293b;
                        border-radius: 16px;
                        padding: 25px;
                        margin-bottom: 20px;
                        transition: all 0.3s ease;
                    }

                    .playlist-card:hover {
                        border-color: #1DB954;
                        box-shadow: 0 4px 20px rgba(29, 185, 84, 0.2);
                    }

                    .playlist-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: start;
                        margin-bottom: 20px;
                        padding-bottom: 20px;
                        border-bottom: 1px solid #1e293b;
                    }

                    .playlist-title {
                        font-size: 22px;
                        font-weight: 700;
                        color: #fff;
                        margin-bottom: 10px;
                    }

                    .playlist-genres {
                        display: flex;
                        gap: 8px;
                        flex-wrap: wrap;
                    }

                    .genre-tag {
                        padding: 6px 14px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 500;
                        background: rgba(29, 185, 84, 0.15);
                        color: #1DB954;
                        border: 1px solid rgba(29, 185, 84, 0.3);
                    }

                    .subgenre-tag {
                        padding: 6px 14px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 500;
                        background: rgba(249, 115, 22, 0.15);
                        color: #fb923c;
                        border: 1px solid rgba(249, 115, 22, 0.3);
                    }

                    .playlist-stats {
                        display: flex;
                        gap: 20px;
                        align-items: center;
                    }

                    .playlist-stat-item {
                        text-align: center;
                    }

                    .playlist-stat-value {
                        font-size: 24px;
                        font-weight: 700;
                        color: #1DB954;
                    }

                    .playlist-stat-label {
                        font-size: 11px;
                        color: #64748b;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-top: 4px;
                    }

                    /* Tracks */
                    .tracks-list {
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }

                    .track-item {
                        background: rgba(30, 41, 59, 0.3);
                        border: 1px solid #1e293b;
                        border-radius: 12px;
                        padding: 16px;
                        display: grid;
                        grid-template-columns: 1fr auto;
                        gap: 20px;
                        align-items: center;
                        transition: all 0.2s ease;
                    }

                    .track-item:hover {
                        background: rgba(30, 41, 59, 0.5);
                        border-color: #334155;
                    }

                    .track-info {
                        display: flex;
                        flex-direction: column;
                        gap: 6px;
                    }

                    .track-name {
                        font-size: 15px;
                        font-weight: 600;
                        color: #fff;
                    }

                    .track-artist {
                        font-size: 13px;
                        color: #94a3b8;
                    }

                    .track-album {
                        font-size: 12px;
                        color: #64748b;
                    }

                    .track-meta {
                        display: flex;
                        gap: 10px;
                        align-items: center;
                    }

                    .track-badge {
                        padding: 6px 12px;
                        border-radius: 8px;
                        font-size: 12px;
                        font-weight: 600;
                    }

                    .track-duration {
                        background: rgba(59, 130, 246, 0.15);
                        color: #60a5fa;
                        border: 1px solid rgba(59, 130, 246, 0.3);
                    }

                    .track-popularity {
                        background: rgba(249, 115, 22, 0.15);
                        color: #fb923c;
                        border: 1px solid rgba(249, 115, 22, 0.3);
                    }

                    .audio-features {
                        grid-column: 1 / -1;
                        margin-top: 12px;
                        padding-top: 12px;
                        border-top: 1px solid #1e293b;
                    }

                    .features-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                        gap: 10px;
                    }

                    .feature-item {
                        background: rgba(30, 41, 59, 0.4);
                        padding: 10px;
                        border-radius: 8px;
                        text-align: center;
                    }

                    .feature-label {
                        font-size: 10px;
                        color: #64748b;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 4px;
                    }

                    .feature-value {
                        font-size: 14px;
                        font-weight: 700;
                        color: #1DB954;
                    }

                    @media (max-width: 1024px) {
                        .dashboard-container {
                            grid-template-columns: 1fr;
                        }

                        .sidebar {
                            position: relative;
                            height: auto;
                            border-right: none;
                            border-bottom: 1px solid #1e293b;
                        }

                        .charts-grid {
                            grid-template-columns: 1fr;
                        }
                    }

                    @media (max-width: 768px) {
                        .main-content {
                            padding: 20px;
                        }

                        .track-item {
                            grid-template-columns: 1fr;
                        }

                        .track-meta {
                            justify-content: flex-start;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="dashboard-container">
                    <!-- Sidebar -->
                    <aside class="sidebar">
                        <div class="logo">
                            <div class="logo-icon">♫</div>
                            <div class="logo-text">Spotify Analytics</div>
                        </div>

                        <div class="sidebar-stats">
                            <div class="sidebar-stat">
                                <div class="sidebar-stat-label">Total Playlists</div>
                                <div class="sidebar-stat-value">
                                    <xsl:value-of select="/spotify_data/@total_playlists"/>
                                </div>
                            </div>

                            <div class="sidebar-stat">
                                <div class="sidebar-stat-label">Total Tracks</div>
                                <div class="sidebar-stat-value">
                                    <xsl:value-of select="/spotify_data/@total_tracks"/>
                                </div>
                            </div>

                            <div class="sidebar-stat">
                                <div class="sidebar-stat-label">Generated</div>
                                <div class="sidebar-stat-sublabel">
                                    <xsl:value-of select="substring(/spotify_data/@generated_at, 1, 10)"/>
                                </div>
                            </div>
                        </div>
                    </aside>

                    <!-- Main Content -->
                    <main class="main-content">
                        <div class="page-header">
                            <h1 class="page-title">Music Library Dashboard</h1>
                            <p class="page-subtitle">Analyse complète de votre collection Spotify</p>
                        </div>

                        <!-- Charts -->
                        <div class="charts-grid">
                            <div class="chart-card">
                                <h3 class="chart-card-title">
                                    <span class="chart-card-title-icon"></span>
                                    Distribution des Playlists
                                </h3>
                                <div class="chart-container">
                                    <canvas id="playlistsChart"></canvas>
                                </div>
                            </div>

                            <div class="chart-card">
                                <h3 class="chart-card-title">
                                    <span class="chart-card-title-icon"></span>
                                    Popularité Moyenne par Playlist
                                </h3>
                                <div class="chart-container">
                                    <canvas id="popularityChart"></canvas>
                                </div>
                            </div>

                            <div class="chart-card">
                                <h3 class="chart-card-title">
                                    <span class="chart-card-title-icon"></span>
                                    Caractéristiques Audio Moyennes
                                </h3>
                                <div class="chart-container">
                                    <canvas id="audioFeaturesChart"></canvas>
                                </div>
                            </div>

                            <div class="chart-card">
                                <h3 class="chart-card-title">
                                    <span class="chart-card-title-icon"></span>
                                    Distribution des Genres
                                </h3>
                                <div class="chart-container">
                                    <canvas id="genresChart"></canvas>
                                </div>
                            </div>
                        </div>

                        <!-- Playlists -->
                        <div class="playlists-section">
                            <h2 class="section-title">Vos Playlists</h2>
                            <xsl:apply-templates select="spotify_data/playlists/playlist"/>
                        </div>
                    </main>
                </div>

                <!-- Data for Charts (hidden) -->
                <script id="chartData" type="application/json">
                    {
                        "playlists": [
                            <xsl:for-each select="spotify_data/playlists/playlist">
                                {
                                    "name": "<xsl:value-of select="nom"/>",
                                    "genre": "<xsl:value-of select="genre"/>",
                                    "trackCount": <xsl:value-of select="tracks/@count"/>,
                                    "avgPopularity": <xsl:value-of select="sum(tracks/track/popularity) div count(tracks/track)"/>,
                                    "avgEnergy": <xsl:value-of select="sum(tracks/track/audio_features/energy) div count(tracks/track[audio_features/energy])"/>,
                                    "avgDanceability": <xsl:value-of select="sum(tracks/track/audio_features/danceability) div count(tracks/track[audio_features/danceability])"/>,
                                    "avgValence": <xsl:value-of select="sum(tracks/track/audio_features/valence) div count(tracks/track[audio_features/valence])"/>
                                }<xsl:if test="position() != last()">,</xsl:if>
                            </xsl:for-each>
                        ]
                    }
                </script>

                <script>
                    // Load chart data
                    const chartDataElement = document.getElementById('chartData');
                    const data = JSON.parse(chartDataElement.textContent);

                    // Common chart config
                    Chart.defaults.color = '#94a3b8';
                    Chart.defaults.borderColor = '#1e293b';

                    // Playlists Distribution Chart
                    new Chart(document.getElementById('playlistsChart'), {
                        type: 'bar',
                        data: {
                            labels: data.playlists.map(p => p.name),
                            datasets: [{
                                label: 'Nombre de tracks',
                                data: data.playlists.map(p => p.trackCount),
                                backgroundColor: 'rgba(29, 185, 84, 0.7)',
                                borderColor: '#1DB954',
                                borderWidth: 2,
                                borderRadius: 8
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    grid: { color: '#1e293b' }
                                },
                                x: {
                                    grid: { display: false }
                                }
                            }
                        }
                    });

                    // Popularity Chart
                    new Chart(document.getElementById('popularityChart'), {
                        type: 'line',
                        data: {
                            labels: data.playlists.map(p => p.name),
                            datasets: [{
                                label: 'Popularité',
                                data: data.playlists.map(p => p.avgPopularity),
                                backgroundColor: 'rgba(251, 146, 60, 0.2)',
                                borderColor: '#fb923c',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 100,
                                    grid: { color: '#1e293b' }
                                },
                                x: {
                                    grid: { display: false }
                                }
                            }
                        }
                    });

                    // Audio Features Radar Chart
                    const avgEnergy = data.playlists.reduce((sum, p) => sum + (p.avgEnergy || 0), 0) / data.playlists.length;
                    const avgDanceability = data.playlists.reduce((sum, p) => sum + (p.avgDanceability || 0), 0) / data.playlists.length;
                    const avgValence = data.playlists.reduce((sum, p) => sum + (p.avgValence || 0), 0) / data.playlists.length;

                    new Chart(document.getElementById('audioFeaturesChart'), {
                        type: 'radar',
                        data: {
                            labels: ['Energy', 'Danceability', 'Valence'],
                            datasets: [{
                                label: 'Moyenne',
                                data: [avgEnergy, avgDanceability, avgValence],
                                backgroundColor: 'rgba(96, 165, 250, 0.2)',
                                borderColor: '#60a5fa',
                                borderWidth: 3,
                                pointBackgroundColor: '#60a5fa'
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false }
                            },
                            scales: {
                                r: {
                                    beginAtZero: true,
                                    max: 1,
                                    grid: { color: '#1e293b' },
                                    ticks: { backdropColor: 'transparent' }
                                }
                            }
                        }
                    });

                    // Genres Distribution
                    const genreCounts = {};
                    data.playlists.forEach(p => {
                        genreCounts[p.genre] = (genreCounts[p.genre] || 0) + 1;
                    });

                    const colors = [
                        '#1DB954', '#60a5fa', '#fb923c', '#a78bfa',
                        '#f472b6', '#fbbf24', '#34d399', '#f87171'
                    ];

                    new Chart(document.getElementById('genresChart'), {
                        type: 'doughnut',
                        data: {
                            labels: Object.keys(genreCounts),
                            datasets: [{
                                data: Object.values(genreCounts),
                                backgroundColor: colors,
                                borderColor: '#0a0e27',
                                borderWidth: 3
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom',
                                    labels: { padding: 15 }
                                }
                            }
                        }
                    });
                </script>
            </body>
        </html>
    </xsl:template>

    <!-- Template pour chaque playlist -->
    <xsl:template match="playlist">
        <div class="playlist-card">
            <div class="playlist-header">
                <div>
                    <div class="playlist-title">
                        <xsl:value-of select="nom"/>
                    </div>
                    <div class="playlist-genres">
                        <span class="genre-tag">
                            <xsl:value-of select="genre"/>
                        </span>
                        <xsl:if test="subgenre != ''">
                            <span class="subgenre-tag">
                                <xsl:value-of select="subgenre"/>
                            </span>
                        </xsl:if>
                    </div>
                </div>

                <div class="playlist-stats">
                    <div class="playlist-stat-item">
                        <div class="playlist-stat-value">
                            <xsl:value-of select="tracks/@count"/>
                        </div>
                        <div class="playlist-stat-label">Tracks</div>
                    </div>
                </div>
            </div>

            <div class="tracks-list">
                <xsl:apply-templates select="tracks/track"/>
            </div>
        </div>
    </xsl:template>

    <!-- Template pour chaque track -->
    <xsl:template match="track">
        <div class="track-item">
            <div class="track-info">
                <div class="track-name">
                    <xsl:value-of select="name"/>
                </div>
                <div class="track-artist">
                    <xsl:value-of select="artist/name"/>
                </div>
                <div class="track-album">
                    <xsl:value-of select="album/name"/>
                    <xsl:if test="album/release_date">
                        · <xsl:value-of select="album/release_date"/>
                    </xsl:if>
                </div>
            </div>

            <div class="track-meta">
                <span class="track-badge track-duration">
                    <xsl:value-of select="duration"/>
                </span>
                <span class="track-badge track-popularity">
                    <xsl:value-of select="popularity"/>
                </span>
            </div>

            <!-- Audio features si disponibles -->
            <xsl:if test="audio_features">
                <div class="audio-features">
                    <div class="features-grid">
                        <xsl:if test="audio_features/energy">
                            <div class="feature-item">
                                <div class="feature-label">Energy</div>
                                <div class="feature-value">
                                    <xsl:value-of select="format-number(audio_features/energy, '0.00')"/>
                                </div>
                            </div>
                        </xsl:if>
                        <xsl:if test="audio_features/danceability">
                            <div class="feature-item">
                                <div class="feature-label">Dance</div>
                                <div class="feature-value">
                                    <xsl:value-of select="format-number(audio_features/danceability, '0.00')"/>
                                </div>
                            </div>
                        </xsl:if>
                        <xsl:if test="audio_features/valence">
                            <div class="feature-item">
                                <div class="feature-label">Valence</div>
                                <div class="feature-value">
                                    <xsl:value-of select="format-number(audio_features/valence, '0.00')"/>
                                </div>
                            </div>
                        </xsl:if>
                        <xsl:if test="audio_features/tempo">
                            <div class="feature-item">
                                <div class="feature-label">Tempo</div>
                                <div class="feature-value">
                                    <xsl:value-of select="format-number(audio_features/tempo, '0')"/> BPM
                                </div>
                            </div>
                        </xsl:if>
                        <xsl:if test="audio_features/loudness">
                            <div class="feature-item">
                                <div class="feature-label">Loudness</div>
                                <div class="feature-value">
                                    <xsl:value-of select="format-number(audio_features/loudness, '0.0')"/> dB
                                </div>
                            </div>
                        </xsl:if>
                    </div>
                </div>
            </xsl:if>
        </div>
    </xsl:template>

</xsl:stylesheet>

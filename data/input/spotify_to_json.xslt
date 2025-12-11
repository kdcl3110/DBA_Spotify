<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" encoding="UTF-8" indent="no"/>

    <!-- Template principal -->
    <xsl:template match="/spotify_data">
        <xsl:text>{</xsl:text>
        <xsl:text>"generated_at": "</xsl:text>
        <xsl:value-of select="@generated_at"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"total_playlists": </xsl:text>
        <xsl:value-of select="@total_playlists"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"total_tracks": </xsl:text>
        <xsl:value-of select="@total_tracks"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"playlists": [</xsl:text>
        <xsl:apply-templates select="playlists/playlist"/>
        <xsl:text>]}</xsl:text>
    </xsl:template>

    <!-- Template pour playlist -->
    <xsl:template match="playlist">
        <xsl:text>{"id": "</xsl:text>
        <xsl:value-of select="@id"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"nom": "</xsl:text>
        <xsl:call-template name="escape-json">
            <xsl:with-param name="text" select="nom"/>
        </xsl:call-template>
        <xsl:text>",</xsl:text>
        <xsl:text>"genre": "</xsl:text>
        <xsl:value-of select="genre"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"subgenre": "</xsl:text>
        <xsl:value-of select="subgenre"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"tracks_count": </xsl:text>
        <xsl:value-of select="tracks/@count"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"tracks": [</xsl:text>
        <xsl:apply-templates select="tracks/track"/>
        <xsl:text>]}</xsl:text>
        <xsl:if test="position() != last()">
            <xsl:text>,</xsl:text>
        </xsl:if>
    </xsl:template>

    <!-- Template pour track -->
    <xsl:template match="track">
        <xsl:text>{"id": "</xsl:text>
        <xsl:value-of select="@id"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"name": "</xsl:text>
        <xsl:call-template name="escape-json">
            <xsl:with-param name="text" select="name"/>
        </xsl:call-template>
        <xsl:text>",</xsl:text>
        <xsl:text>"duration_ms": </xsl:text>
        <xsl:value-of select="duration/@ms"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"duration_formatted": "</xsl:text>
        <xsl:value-of select="duration"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"popularity": </xsl:text>
        <xsl:value-of select="popularity"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"album": {</xsl:text>
        <xsl:text>"id": "</xsl:text>
        <xsl:value-of select="album/@id"/>
        <xsl:text>",</xsl:text>
        <xsl:text>"name": "</xsl:text>
        <xsl:call-template name="escape-json">
            <xsl:with-param name="text" select="album/name"/>
        </xsl:call-template>
        <xsl:text>",</xsl:text>
        <xsl:text>"release_date": "</xsl:text>
        <xsl:value-of select="album/release_date"/>
        <xsl:text>"},</xsl:text>
        <xsl:text>"artist": {</xsl:text>
        <xsl:text>"name": "</xsl:text>
        <xsl:call-template name="escape-json">
            <xsl:with-param name="text" select="artist/name"/>
        </xsl:call-template>
        <xsl:text>"},</xsl:text>
        <xsl:text>"audio_features": {</xsl:text>
        <xsl:text>"energy": </xsl:text>
        <xsl:value-of select="audio_features/energy"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"tempo": </xsl:text>
        <xsl:value-of select="audio_features/tempo"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"danceability": </xsl:text>
        <xsl:value-of select="audio_features/danceability"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"loudness": </xsl:text>
        <xsl:value-of select="audio_features/loudness"/>
        <xsl:text>,</xsl:text>
        <xsl:text>"valence": </xsl:text>
        <xsl:value-of select="audio_features/valence"/>
        <xsl:text>}}</xsl:text>
        <xsl:if test="position() != last()">
            <xsl:text>,</xsl:text>
        </xsl:if>
    </xsl:template>

    <!-- Template pour échapper les caractères spéciaux JSON -->
    <xsl:template name="escape-json">
        <xsl:param name="text"/>
        <xsl:variable name="escaped-quotes">
            <xsl:call-template name="replace-string">
                <xsl:with-param name="text" select="$text"/>
                <xsl:with-param name="from" select="'&quot;'"/>
                <xsl:with-param name="to" select="'\&quot;'"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="escaped-backslash">
            <xsl:call-template name="replace-string">
                <xsl:with-param name="text" select="$escaped-quotes"/>
                <xsl:with-param name="from" select="'\'"/>
                <xsl:with-param name="to" select="'\\'"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:value-of select="$escaped-backslash"/>
    </xsl:template>

    <!-- Template utilitaire pour remplacer des chaînes -->
    <xsl:template name="replace-string">
        <xsl:param name="text"/>
        <xsl:param name="from"/>
        <xsl:param name="to"/>
        <xsl:choose>
            <xsl:when test="contains($text, $from)">
                <xsl:value-of select="substring-before($text, $from)"/>
                <xsl:value-of select="$to"/>
                <xsl:call-template name="replace-string">
                    <xsl:with-param name="text" select="substring-after($text, $from)"/>
                    <xsl:with-param name="from" select="$from"/>
                    <xsl:with-param name="to" select="$to"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$text"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>

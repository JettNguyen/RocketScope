import { useState, useEffect, useMemo } from 'react'
import './index.css'

function App() {
  const [data, setData] = useState(null)
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('./data/mentions.json')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load data')
        return res.json()
      })
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const results = useMemo(() => {
    if (!data || !query.trim()) return []
    const q = query.toLowerCase().trim()
    
    return data.videos
      .map(video => {
        const matchingMentions = {}
        for (const [player, mentions] of Object.entries(video.mentions)) {
          if (player.toLowerCase().includes(q)) {
            matchingMentions[player] = mentions
          }
        }
        if (Object.keys(matchingMentions).length === 0) return null
        return { ...video, mentions: matchingMentions }
      })
      .filter(Boolean)
  }, [data, query])

  const stats = useMemo(() => {
    if (!results.length) return null
    const totalMentions = results.reduce((acc, v) => 
      acc + Object.values(v.mentions).reduce((a, m) => a + m.length, 0), 0
    )
    const players = [...new Set(results.flatMap(v => Object.keys(v.mentions)))]
    return { totalMentions, players, videoCount: results.length }
  }, [results])

  const topPlayers = useMemo(() => {
    if (!data) return []
    const counts = {}
    for (const video of data.videos) {
      for (const [player, mentions] of Object.entries(video.mentions)) {
        counts[player] = (counts[player] || 0) + mentions.length
      }
    }
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 12)
      .map(([name]) => name)
  }, [data])

  const formatTimestamp = (seconds) => {
    const h = Math.floor(seconds / 3600)
    const m = Math.floor((seconds % 3600) / 60)
    const s = seconds % 60
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
    return `${m}:${s.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading data...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">
          <h2>Error loading data</h2>
          <p>{error}</p>
          <p>Run the indexer to generate mentions.json</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <header>
        <h1>Rocket League Player Mentions</h1>
        <p className="subtitle">
          Track player mentions across Rocket League YouTube videos
        </p>
        <p className="meta">
          {data.videos.length} videos indexed • Last updated: {new Date(data.lastUpdated).toLocaleDateString()}
        </p>
      </header>

      <div className="search-box">
        <input
          type="text"
          placeholder="Search for a player name..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          autoFocus
        />
      </div>

      <div className="quick-search">
        <span>Popular:</span>
        {topPlayers.map(player => (
          <button key={player} onClick={() => setQuery(player)}>
            {player}
          </button>
        ))}
      </div>

      {stats && (
        <div className="stats">
          Found <strong>{stats.totalMentions}</strong> mentions in{' '}
          <strong>{stats.videoCount}</strong> videos
        </div>
      )}

      <div className="results">
        {query && results.length === 0 && (
          <div className="no-results">
            No mentions found for "{query}"
          </div>
        )}

        {results.map(video => (
          <div key={video.videoId} className="video-card">
            <a
              href={`https://youtube.com/watch?v=${video.videoId}`}
              target="_blank"
              rel="noopener noreferrer"
              className="video-link"
            >
              <img
                src={video.thumbnail}
                alt={video.title}
                className="thumbnail"
              />
              <div className="video-info">
                <h3>{video.title}</h3>
                <p className="video-meta">
                  {video.channel} • {video.date}
                </p>
              </div>
            </a>
            
            <div className="mentions">
              {Object.entries(video.mentions).map(([player, mentions]) => (
                <div key={player} className="player-mentions">
                  <div className="player-name">{player}</div>
                  <div className="timestamps">
                    {mentions.map((m, i) => (
                      <a
                        key={i}
                        href={`https://youtube.com/watch?v=${video.videoId}&t=${m.seconds}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="timestamp"
                        title={m.text}
                      >
                        {m.time}
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <footer>
        <p>
          Data sourced from YouTube transcripts •{' '}
          <a href="https://github.com/JettNguyen/RocketScope">GitHub</a>
        </p>
      </footer>
    </div>
  )
}

export default App
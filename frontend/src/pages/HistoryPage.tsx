import { useState, useEffect } from 'react'
import type { PredictionHistory } from '../types'

function HistoryPage() {
  const [history, setHistory] = useState<PredictionHistory[]>([])
  const [filter, setFilter] = useState<string>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHistory()
  }, [filter])

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const url = filter === 'all' ? '/history?limit=100' : `/history?limit=100&model_name=${filter}`
      const response = await fetch(url)
      const data = await response.json()
      setHistory(data)
    } catch (error) {
      console.error('Error fetching history:', error)
    } finally {
      setLoading(false)
    }
  }

  const modelIcons: Record<string, string> = {
    salary: '💰',
    house: '🏠',
    crop: '🌾',
    stock: '📈',
    weather: '🌤️'
  }

  const filteredHistory = filter === 'all' 
    ? history 
    : history.filter(h => h.model_name === filter)

  return (
    <div className="fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-4xl font-bold font-orbitron gradient-text mb-2">
            Prediction History
          </h2>
          <p className="text-gray-400">View all your past predictions</p>
        </div>

        {/* Filter */}
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-black/50 border-2 border-purple-500/30 rounded-xl px-4 py-3 focus:border-purple-500 focus:outline-none"
        >
          <option value="all">All Models</option>
          <option value="salary">💰 Salary</option>
          <option value="house">🏠 House</option>
          <option value="crop">🌾 Crop</option>
          <option value="stock">📈 Stock</option>
          <option value="weather">🌤️ Weather</option>
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="spinner"></div>
        </div>
      ) : filteredHistory.length === 0 ? (
        <div className="glass-card rounded-2xl p-12 text-center">
          <div className="text-6xl mb-4 opacity-30">📊</div>
          <p className="text-xl text-gray-400">No predictions yet</p>
          <p className="text-sm text-gray-500 mt-2">Start making predictions to see your history</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredHistory.map((item) => (
            <div
              key={item.id}
              className="glass-card rounded-xl p-6 hover:border-purple-500/50 transition-all"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4 flex-1">
                  <div className="text-4xl">{modelIcons[item.model_name] || '🔮'}</div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold font-orbitron capitalize">
                        {item.model_name}
                      </h3>
                      <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-full text-xs font-semibold">
                        {item.model_version}
                      </span>
                    </div>
                    
                    {/* Input Data */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                      {Object.entries(item.input_data).map(([key, value]) => (
                        <div key={key} className="bg-black/30 rounded-lg px-3 py-2">
                          <div className="text-xs text-gray-500 capitalize">
                            {key.replace(/_/g, ' ')}
                          </div>
                          <div className="text-sm font-semibold">{String(value)}</div>
                        </div>
                      ))}
                    </div>

                    <div className="text-xs text-gray-500">
                      {new Date(item.created_at).toLocaleString()}
                    </div>
                  </div>
                </div>

                {/* Prediction Result */}
                <div className="text-right ml-6">
                  <div className="text-sm text-gray-400 mb-1">Prediction</div>
                  <div className="text-3xl font-bold font-orbitron gradient-text">
                    {item.prediction.toLocaleString()}
                  </div>
                  {item.confidence && (
                    <div className="text-xs text-gray-500 mt-1">
                      {(item.confidence * 100).toFixed(1)}% confidence
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default HistoryPage

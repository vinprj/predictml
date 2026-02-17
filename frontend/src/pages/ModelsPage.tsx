import { useState, useEffect, useCallback } from 'react'
import type { ModelVersion } from '../types'

const FAVORITES_KEY = 'predictml_favorites'

function ModelsPage() {
  const [models, setModels] = useState<ModelVersion[]>([])
  const [loading, setLoading] = useState(true)
  const [favorites, setFavorites] = useState<string[]>([])
  const [filter, setFilter] = useState<'all' | 'favorites'>('all')

  // Load favorites from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(FAVORITES_KEY)
    if (saved) {
      try {
        setFavorites(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load favorites:', e)
      }
    }
  }, [])

  // Save favorites to localStorage
  const toggleFavorite = useCallback((modelName: string) => {
    setFavorites(prev => {
      const updated = prev.includes(modelName)
        ? prev.filter(f => f !== modelName)
        : [...prev, modelName]
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated))
      return updated
    })
  }, [])

  useEffect(() => {
    fetch('/models')
      .then(res => res.json())
      .then(setModels)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const modelInfo: Record<string, { icon: string; gradient: string; description: string }> = {
    salary: {
      icon: '💰',
      gradient: 'from-green-500 to-emerald-600',
      description: 'Linear Regression model for salary prediction based on experience'
    },
    house: {
      icon: '🏠',
      gradient: 'from-blue-500 to-cyan-600',
      description: 'Random Forest model for house price estimation'
    },
    crop: {
      icon: '🌾',
      gradient: 'from-yellow-500 to-orange-600',
      description: 'Decision Tree model for crop yield forecasting'
    },
    stock: {
      icon: '📈',
      gradient: 'from-purple-500 to-pink-600',
      description: 'LSTM-based model for stock price prediction'
    },
    weather: {
      icon: '🌤️',
      gradient: 'from-cyan-500 to-blue-600',
      description: 'Random Forest model for weather forecasting'
    }
  }

  const displayedModels = filter === 'favorites' 
    ? models.filter(m => favorites.includes(m.model_name))
    : models

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div className="fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-4xl font-bold font-orbitron gradient-text mb-3">
            Model Versions
          </h2>
          <p className="text-gray-400">
            Explore our AI models and their performance metrics
          </p>
        </div>
        
        {/* Filter Tabs */}
        <div className="glass-card rounded-full px-2 py-1 flex gap-1">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${
              filter === 'all' 
                ? 'bg-gradient-to-r from-purple-600 to-blue-500 text-white' 
                : 'text-gray-400 hover:text-white'
            }`}
          >
            All Models ({models.length})
          </button>
          <button
            onClick={() => setFilter('favorites')}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all flex items-center gap-2 ${
              filter === 'favorites' 
                ? 'bg-gradient-to-r from-purple-600 to-blue-500 text-white' 
                : 'text-gray-400 hover:text-white'
            }`}
          >
            ⭐ Favorites ({favorites.length})
          </button>
        </div>
      </div>

      {displayedModels.length === 0 && filter === 'favorites' ? (
        <div className="text-center py-20 glass-card rounded-2xl">
          <div className="text-6xl mb-4">⭐</div>
          <h3 className="text-2xl font-bold font-orbitron text-white mb-2">No Favorites Yet</h3>
          <p className="text-gray-400 mb-4">Star your favorite models to see them here</p>
          <button
            onClick={() => setFilter('all')}
            className="text-purple-400 hover:text-purple-300 font-semibold"
          >
            Browse All Models →
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayedModels.map((model) => {
            const info = modelInfo[model.model_name] || { icon: '🤖', gradient: 'from-gray-500 to-gray-600', description: '' }
            const isFavorite = favorites.includes(model.model_name)
            
            return (
              <div
                key={model.id}
                className="glass-card rounded-2xl p-6 holo-border group hover:scale-105 transition-all relative"
              >
                {/* Favorite Button */}
                <button
                  onClick={() => toggleFavorite(model.model_name)}
                  className={`absolute top-4 right-4 text-2xl transition-all hover:scale-110 ${
                    isFavorite ? 'text-yellow-400' : 'text-gray-600 hover:text-gray-400'
                  }`}
                  title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                >
                  {isFavorite ? '★' : '☆'}
                </button>

                {/* Icon & Status */}
                <div className="flex justify-between items-start mb-6">
                  <div className="text-5xl">{info.icon}</div>
                  <div className="px-3 py-1 bg-green-500/20 text-green-300 rounded-full text-xs font-bold">
                    ACTIVE
                  </div>
                </div>

                {/* Title */}
                <h3 className="text-2xl font-bold font-orbitron capitalize mb-2 group-hover:gradient-text transition-all">
                  {model.model_name}
                </h3>

                {/* Description */}
                <p className="text-sm text-gray-400 mb-6 leading-relaxed">
                  {model.description || info.description}
                </p>

                {/* Version Badge */}
                <div className={`inline-block px-4 py-2 rounded-full bg-gradient-to-r ${info.gradient} text-white text-sm font-semibold mb-6`}>
                  Version {model.current_version}
                </div>

                {/* Metrics */}
                <div className="grid grid-cols-2 gap-4">
                  {model.accuracy && (
                    <div className="bg-black/30 rounded-lg p-3">
                      <div className="text-xs text-gray-500 mb-1">Accuracy</div>
                      <div className="text-2xl font-bold font-orbitron gradient-text">
                        {(model.accuracy * 100).toFixed(1)}%
                      </div>
                    </div>
                  )}
                  <div className="bg-black/30 rounded-lg p-3">
                    <div className="text-xs text-gray-500 mb-1">Updated</div>
                    <div className="text-sm font-semibold">
                      {new Date(model.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                {/* Training Date */}
                <div className="mt-4 pt-4 border-t border-white/10 text-xs text-gray-500">
                  Created: {new Date(model.created_at).toLocaleDateString()}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Footer Info */}
      <div className="mt-12 glass-card rounded-2xl p-8">
        <h3 className="text-2xl font-bold font-orbitron mb-4">About Our Models</h3>
        <div className="grid md:grid-cols-2 gap-6 text-sm text-gray-400">
          <div>
            <h4 className="font-semibold text-white mb-2">🔄 Continuous Improvement</h4>
            <p>
              Our models are regularly updated and retrained with new data to ensure optimal accuracy and performance.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-2">📊 Version Control</h4>
            <p>
              We maintain version history for all models, allowing us to track improvements and roll back if needed.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-2">🎯 Validated Results</h4>
            <p>
              All models undergo rigorous testing and validation before deployment to ensure reliable predictions.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-2">⚡ Real-time Processing</h4>
            <p>
              Lightning-fast inference engine delivers predictions in milliseconds, no matter the complexity.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModelsPage

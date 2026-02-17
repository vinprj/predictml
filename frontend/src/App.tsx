import { useState, useEffect, useCallback } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import PredictPage from './pages/PredictPage'
import HistoryPage from './pages/HistoryPage'
import ModelsPage from './pages/ModelsPage'
import type { HistoryStats } from './types'

const FAVORITES_KEY = 'predictml_favorites'

function Navigation() {
  const location = useLocation()
  
  const isActive = (path: string) => {
    return location.pathname === path
      ? 'bg-gradient-to-r from-purple-600 to-blue-500 text-white'
      : 'text-gray-300 hover:text-white hover:bg-white/10'
  }

  return (
    <nav className="glass-card rounded-full px-6 py-3 flex gap-2">
      <Link
        to="/"
        className={`px-6 py-2 rounded-full font-semibold transition-all ${isActive('/')}`}
      >
        🔮 Predict
      </Link>
      <Link
        to="/history"
        className={`px-6 py-2 rounded-full font-semibold transition-all ${isActive('/history')}`}
      >
        📊 History
      </Link>
      <Link
        to="/models"
        className={`px-6 py-2 rounded-full font-semibold transition-all ${isActive('/models')}`}
      >
        🤖 Models
      </Link>
    </nav>
  )
}

function ApiStatus() {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking')
  const [latency, setLatency] = useState<number | null>(null)

  useEffect(() => {
    const checkStatus = async () => {
      const start = Date.now()
      try {
        const res = await fetch('/health', { method: 'GET' })
        if (res.ok) {
          setStatus('connected')
          setLatency(Date.now() - start)
        } else {
          setStatus('disconnected')
        }
      } catch {
        setStatus('disconnected')
      }
    }

    checkStatus()
    const interval = setInterval(checkStatus, 10000)
    return () => clearInterval(interval)
  }, [])

  const getStatusColor = () => {
    switch (status) {
      case 'connected': return 'bg-green-500'
      case 'disconnected': return 'bg-red-500'
      default: return 'bg-yellow-500'
    }
  }

  return (
    <div className="glass-card rounded-2xl px-4 py-2 flex items-center gap-3">
      <div className={`w-2.5 h-2.5 rounded-full ${getStatusColor()} ${status === 'connected' ? 'pulse-orb' : ''}`}></div>
      <div className="text-xs font-orbitron text-gray-300">
        {status === 'connected' ? (
          <>API <span className="text-cyan-400">{latency}ms</span></>
        ) : status === 'checking' ? (
          <span className="text-yellow-400">CHECKING...</span>
        ) : (
          <span className="text-red-400">OFFLINE</span>
        )}
      </div>
    </div>
  )
}

function Layout({ children }: { children: React.ReactNode }) {
  const [stats, setStats] = useState<HistoryStats | null>(null)
  const [favorites, setFavorites] = useState<string[]>([])

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
    fetch('/history/stats')
      .then(res => res.json())
      .then(setStats)
      .catch(console.error)
  }, [])

  return (
    <div className="min-h-screen relative z-10">
      {/* Header */}
      <header className="border-b border-purple-500/20 backdrop-blur-sm sticky top-0 z-50 bg-gradient-to-b from-black/50 to-transparent">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-5xl font-bold font-orbitron gradient-text neon-glow mb-2">
                PREDICT ML
              </h1>
              <p className="text-gray-400 text-sm font-light">
                AI-Powered Prediction Service • v2.1
              </p>
            </div>
            <div className="flex items-center gap-4">
              <ApiStatus />
              {stats && (
                <div className="glass-card rounded-2xl px-6 py-3">
                  <div className="text-sm text-gray-400 mb-1">Total Predictions</div>
                  <div className="text-3xl font-bold font-orbitron gradient-text">
                    {stats.total_predictions.toLocaleString()}
                  </div>
                </div>
              )}
            </div>
          </div>
          <Navigation />
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-12">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-purple-500/20 mt-20 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-500 text-sm">
          <p>PredictML • Powered by Machine Learning • MIT License</p>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<PredictPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/models" element={<ModelsPage />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

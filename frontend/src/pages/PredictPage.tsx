import { useState } from 'react'
import type { ModelConfig } from '../types'

const MODELS: ModelConfig[] = [
  {
    name: 'salary',
    displayName: 'Salary Prediction',
    description: 'Predict salary based on years of experience',
    icon: '💰',
    gradient: 'from-green-500 to-emerald-600',
    fields: [
      { name: 'years_experience', label: 'Years of Experience', type: 'number', min: 0, max: 50, step: 0.5, placeholder: '5.0' }
    ]
  },
  {
    name: 'house',
    displayName: 'House Price Prediction',
    description: 'Estimate house prices based on features',
    icon: '🏠',
    gradient: 'from-blue-500 to-cyan-600',
    fields: [
      { name: 'area', label: 'Area (sq ft)', type: 'number', min: 100, max: 10000, placeholder: '2000' },
      { name: 'bedrooms', label: 'Bedrooms', type: 'number', min: 1, max: 10, placeholder: '3' },
      { name: 'location', label: 'Location', type: 'select', options: ['rural', 'suburban', 'urban'] }
    ]
  },
  {
    name: 'crop',
    displayName: 'Crop Yield Prediction',
    description: 'Forecast crop yield from weather data',
    icon: '🌾',
    gradient: 'from-yellow-500 to-orange-600',
    fields: [
      { name: 'rainfall', label: 'Rainfall (mm)', type: 'number', min: 0, max: 500, placeholder: '100' },
      { name: 'temperature', label: 'Temperature (°C)', type: 'number', min: -10, max: 50, placeholder: '25' }
    ]
  },
  {
    name: 'stock',
    displayName: 'Stock Price Prediction',
    description: 'Predict future stock prices',
    icon: '📈',
    gradient: 'from-purple-500 to-pink-600',
    fields: [
      { name: 'current_price', label: 'Current Price ($)', type: 'number', min: 0, step: 0.01, placeholder: '150.50' },
      { name: 'days_ahead', label: 'Days Ahead', type: 'number', min: 1, max: 30, placeholder: '7' }
    ]
  },
  {
    name: 'weather',
    displayName: 'Weather Prediction',
    description: 'Forecast temperature and conditions',
    icon: '🌤️',
    gradient: 'from-cyan-500 to-blue-600',
    fields: [
      { name: 'current_temp', label: 'Current Temp (°C)', type: 'number', min: -50, max: 60, placeholder: '22' },
      { name: 'current_humidity', label: 'Current Humidity (%)', type: 'number', min: 0, max: 100, placeholder: '65' },
      { name: 'days_ahead', label: 'Days Ahead', type: 'number', min: 1, max: 14, placeholder: '3' }
    ]
  }
]

function PredictPage() {
  const [selectedModel, setSelectedModel] = useState<ModelConfig | null>(null)
  const [formData, setFormData] = useState<Record<string, any>>({})
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handlePredict = async () => {
    if (!selectedModel) return

    setLoading(true)
    setResult(null)

    try {
      const response = await fetch(`/predict/${selectedModel.name}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) throw new Error('Prediction failed')

      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Error:', error)
      alert('Prediction failed. Please check your inputs.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setSelectedModel(null)
    setFormData({})
    setResult(null)
  }

  return (
    <div className="fade-in">
      {!selectedModel ? (
        <>
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold font-orbitron mb-3">
              Select a <span className="gradient-text">Prediction Model</span>
            </h2>
            <p className="text-gray-400">
              Choose from our AI-powered prediction models
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {MODELS.map((model) => (
              <button
                key={model.name}
                onClick={() => setSelectedModel(model)}
                className="glass-card rounded-2xl p-6 text-left group transition-all hover:scale-105 energy-beam"
              >
                <div className="text-5xl mb-4">{model.icon}</div>
                <h3 className="text-2xl font-bold font-orbitron mb-2 group-hover:gradient-text transition-all">
                  {model.displayName}
                </h3>
                <p className="text-gray-400 text-sm mb-4">{model.description}</p>
                <div className={`inline-block px-4 py-2 rounded-full bg-gradient-to-r ${model.gradient} text-white text-sm font-semibold`}>
                  Activate Model →
                </div>
              </button>
            ))}
          </div>
        </>
      ) : (
        <div className="max-w-2xl mx-auto slide-up">
          <button
            onClick={handleReset}
            className="mb-6 text-gray-400 hover:text-white transition-colors flex items-center gap-2"
          >
            ← Back to Models
          </button>

          <div className="glass-card rounded-2xl p-8 holo-border">
            <div className="flex items-center gap-4 mb-8">
              <div className="text-6xl">{selectedModel.icon}</div>
              <div>
                <h2 className="text-3xl font-bold font-orbitron gradient-text">
                  {selectedModel.displayName}
                </h2>
                <p className="text-gray-400">{selectedModel.description}</p>
              </div>
            </div>

            {/* Input Form */}
            <div className="space-y-6 mb-8">
              {selectedModel.fields.map((field) => (
                <div key={field.name}>
                  <label className="block text-sm font-semibold mb-2 text-gray-300">
                    {field.label}
                  </label>
                  {field.type === 'select' ? (
                    <select
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                      className="w-full bg-black/50 border-2 border-purple-500/30 rounded-xl px-4 py-3 focus:border-purple-500 focus:outline-none transition-all"
                    >
                      <option value="">Select {field.label}</option>
                      {field.options?.map((opt) => (
                        <option key={opt} value={opt}>{opt}</option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type="number"
                      value={formData[field.name] || ''}
                      onChange={(e) => setFormData({ ...formData, [field.name]: parseFloat(e.target.value) || '' })}
                      min={field.min}
                      max={field.max}
                      step={field.step || 1}
                      placeholder={field.placeholder}
                      className="w-full bg-black/50 border-2 border-purple-500/30 rounded-xl px-4 py-3 focus:border-purple-500 focus:outline-none transition-all"
                    />
                  )}
                </div>
              ))}
            </div>

            {/* Predict Button */}
            <button
              onClick={handlePredict}
              disabled={loading}
              className={`w-full bg-gradient-to-r ${selectedModel.gradient} text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed energy-beam font-orbitron`}
            >
              {loading ? (
                <div className="flex items-center justify-center gap-3">
                  <div className="spinner"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                '🔮 Generate Prediction'
              )}
            </button>

            {/* Result */}
            {result && (
              <div className="mt-8 glass-card rounded-xl p-6 border-2 border-green-500/50 slide-up">
                <div className="text-center">
                  <div className="text-sm text-gray-400 mb-2">Predicted Result</div>
                  <div className="text-5xl font-bold font-orbitron gradient-text mb-4">
                    {Object.entries(result)
                      .filter(([key]) => key.includes('predicted'))
                      .map(([_, value]) => typeof value === 'number' ? value.toLocaleString() : value)}
                  </div>
                  <div className="flex justify-center gap-4 text-sm text-gray-400">
                    <div>Model: {result.model}</div>
                    <div>•</div>
                    <div>Version: {result.version}</div>
                    {result.confidence && (
                      <>
                        <div>•</div>
                        <div>Confidence: {(result.confidence * 100).toFixed(1)}%</div>
                      </>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default PredictPage

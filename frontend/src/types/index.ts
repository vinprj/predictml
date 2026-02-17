export interface PredictionHistory {
  id: number
  model_name: string
  model_version: string
  input_data: Record<string, any>
  prediction: number
  confidence?: number
  created_at: string
}

export interface ModelVersion {
  id: number
  model_name: string
  current_version: string
  description?: string
  accuracy?: number
  created_at: string
  updated_at: string
}

export interface HistoryStats {
  total_predictions: number
  predictions_by_model: Record<string, number>
}

export interface ModelConfig {
  name: string
  displayName: string
  description: string
  icon: string
  gradient: string
  fields: Field[]
}

export interface Field {
  name: string
  label: string
  type: 'number' | 'select'
  options?: string[]
  min?: number
  max?: number
  step?: number
  placeholder?: string
}

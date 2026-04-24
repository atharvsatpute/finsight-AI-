import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_URL,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const key = import.meta.env.VITE_API_KEY
  if (key) config.headers['x-api-key'] = key
  return config
})

client.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.detail || err.message || 'Request failed'
    return Promise.reject(new Error(msg))
  }
)

export const api = {
  health: () => client.get('/health'),

  analyze: (query, topK = 8) =>
    client.post('/analyze', { query, top_k: topK }),

  retrieve: (query, topK = 8) =>
    client.post('/retrieve', { query, top_k: topK }),

  ingest: (documents, docType = 'news') =>
    client.post('/ingest', { documents, doc_type: docType }),
}

export default client

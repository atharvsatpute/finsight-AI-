import { useState, useEffect, useCallback, useRef } from 'react'
import { api } from '../services/api'

export function useFinSight() {
  const [query, setQuery] = useState('What are HSBC\'s key risks in the current rate environment?')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [health, setHealth] = useState(null)
  const [agentStates, setAgentStates] = useState({
    risk: 'idle',
    sentiment: 'idle',
    portfolio: 'idle',
  })
  const timersRef = useRef([])

  const clearTimers = () => {
    timersRef.current.forEach(clearTimeout)
    timersRef.current = []
  }

  const fetchHealth = useCallback(async () => {
    try {
      const data = await api.health()
      setHealth(data)
    } catch {
      setHealth(null)
    }
  }, [])

  useEffect(() => {
    fetchHealth()
    const interval = setInterval(fetchHealth, 30000)
    return () => clearInterval(interval)
  }, [fetchHealth])

  const simulateAgents = () => {
    setAgentStates({ risk: 'idle', sentiment: 'idle', portfolio: 'idle' })
    const t1 = setTimeout(() => setAgentStates(s => ({ ...s, risk: 'running' })), 200)
    const t2 = setTimeout(() => setAgentStates(s => ({ ...s, sentiment: 'running' })), 800)
    const t3 = setTimeout(() => setAgentStates(s => ({ ...s, portfolio: 'running' })), 1600)
    timersRef.current = [t1, t2, t3]
  }

  const analyze = useCallback(async (q) => {
    const queryText = q || query
    if (!queryText.trim()) return
    clearTimers()
    setLoading(true)
    setError(null)
    setResult(null)
    simulateAgents()
    try {
      const data = await api.analyze(queryText)
      setResult(data)
      setAgentStates({ risk: 'done', sentiment: 'done', portfolio: 'done' })
    } catch (err) {
      setError(err.message)
      setAgentStates({ risk: 'error', sentiment: 'error', portfolio: 'error' })
    } finally {
      setLoading(false)
    }
  }, [query])

  const reset = useCallback(() => {
    clearTimers()
    setResult(null)
    setError(null)
    setAgentStates({ risk: 'idle', sentiment: 'idle', portfolio: 'idle' })
  }, [])

  return {
    query, setQuery,
    loading, result, error,
    health, agentStates,
    analyze, reset, fetchHealth,
  }
}

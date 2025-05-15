'use client'

import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post('/api/ask', { text: query })
      setResult(response.data)
    } catch (err: any) {
      console.error('API Error:', err)
      if (err.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setError(`Error: ${err.response.data?.detail || err.response.statusText || 'Server error'}`)
      } else if (err.request) {
        // The request was made but no response was received
        setError('Error: No response from server. Please check if the backend is running.')
      } else {
        // Something happened in setting up the request that triggered an Error
        setError(`Error: ${err.message || 'An unexpected error occurred'}`)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-8">EU AI Act Query Interface</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <label htmlFor="query" className="block text-sm font-medium mb-2">
            Enter your question about the EU AI Act
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows={4}
            placeholder="Example: What are the key requirements for high-risk AI systems?"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 disabled:bg-blue-300 transition-colors"
        >
          {loading ? 'Processing...' : 'Submit Question'}
        </button>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-gray-50 p-6 rounded-md shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Answer:</h2>
          <p className="mb-6 text-gray-800 leading-relaxed">{result.answer}</p>
          
          <h3 className="text-lg font-semibold mb-3">Relevant Sources:</h3>
          <div className="space-y-4">
            {result.chunks.map((chunk: any, index: number) => (
              <div key={index} className="bg-white p-4 rounded border border-gray-200 shadow-sm">
                <p className="text-gray-700 mb-2">{chunk.text}</p>
                <div className="text-sm text-gray-500">
                  <p>Source: {chunk.metadata?.source || 'Unknown'}</p>
                  <p>Relevance Score: {(1 - chunk.distance).toFixed(2)}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
} 
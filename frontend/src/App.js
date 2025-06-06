import React, { useState } from 'react';
import GraphExplorer from './GraphExplorer';

function App() {
  const [query, setQuery] = useState('');
  const [hypotheses, setHypotheses] = useState([]);
  const [error, setError] = useState('');

  const handleQuery = async () => {
    if (!query) {
      setError('Please enter a query');
      return;
    }
    try {
      const response = await fetch('http://localhost:8000/generateHypotheses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodes: [query] }),
      });
      if (!response.ok) throw new Error('Failed to fetch hypotheses');
      const data = await response.json();
      setHypotheses(data.hypotheses || []);
      setError('');
    } catch (err) {
      setError('Error: ' + err.message);
      setHypotheses([]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center text-blue-800 mb-6">
        DiaGraph - Diabetes Hypothesis Generator
      </h1>

      <GraphExplorer />

      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Query Graph</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., HNF1A"
          className="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleQuery}
          className="mt-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          Generate Hypotheses
        </button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
        </div>

      {hypotheses.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">Hypotheses</h2>
          {hypotheses.map((hyp, idx) => (
            <div key={idx} className="p-4 bg-white rounded shadow-md mb-2">
              <p><strong>Hypothesis:</strong> {hyp.source} may alter {hyp.target} dynamics.</p>
              <p><strong>Score:</strong> {hyp.score}</p>
              <p><strong>Rationale:</strong> {hyp.rationale}</p>
              <p><strong>Next Steps:</strong> {hyp.nextSteps}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
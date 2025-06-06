import React, { useEffect, useState, useRef } from 'react';
import cytoscape from 'cytoscape';

function GraphExplorer() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const cyRef = useRef(null);

  useEffect(() => {
    let cy;
    setLoading(true);
    fetch('http://localhost:8000/graph')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        cy = cytoscape({
          container: cyRef.current,
          elements: [...(data.nodes || []), ...(data.edges || [])],
          style: [
            {
              selector: 'node',
              style: {
                'background-color': '#3b82f6',
                'label': 'data(label)',
                'color': '#fff',
                'text-outline-width': 2,
                'text-outline-color': '#000',
              },
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'line-color': '#ccc',
                'label': 'data(label)',
                'color': '#000',
                'text-outline-width': 2,
                'text-outline-color': '#fff',
              },
            },
            { selector: 'node[type="Gene"]', style: { 'background-color': '#3b82f6' } },
            { selector: 'node[type="Disease"]', style: { 'background-color': '#ef4444' } },
            { selector: 'node[type="ClinicalTrial"]', style: { 'background-color': '#f59e0b' } },
            { selector: 'node[type="Drug"]', style: { 'background-color': '#8b5cf6' } },
          ],
          layout: { name: 'grid', fit: true, padding: 30 }, // Changed to 'grid' for testing
        });

        cy.on('click', 'node', (evt) => {
          setSelectedNode(evt.target.data());
        });

        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching graph:', err);
        setError(err.message);
        setLoading(false);
      });

    return () => {
      if (cy) cy.destroy();
    };
  }, []);

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-2">Graph Explorer</h2>
      {loading && <p className="text-gray-500">Loading graph...</p>}
      {error && <p className="text-red-500">Error: {error}</p>}
      <div ref={cyRef} id="cy" className="w-full h-[500px] border border-gray-200 rounded" />
      {selectedNode && (
        <div className="node-info mt-4 p-4 bg-gray-50 rounded shadow-md">
          <h3 className="text-lg font-semibold">Node: {selectedNode.label || 'Unknown'}</h3>
          <p><strong>Type:</strong> {selectedNode.type || 'N/A'}</p>
        </div>
      )}
    </div>
  );
}

export default GraphExplorer;
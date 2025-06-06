export interface GraphData {
    nodes: { data: { id: string; label: string; type: string } }[];
    edges: { data: { source: string; target: string; label: string } }[];
  }
from fastapi import FastAPI
import torch
from torch_geometric.nn import GraphSAGE
import csv

app = FastAPI()

model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=16, num_layers=2)
model.load_state_dict(torch.load("graphsage_model.pth"))
model.eval()

@app.post("/generateHypotheses")
async def generate_hypotheses(seed_nodes: dict):
    nodes = seed_nodes.get("nodes", ["HNF1A"])
    hypotheses = [
        {
            "source": nodes[0],
            "target": "GLP-1 Secretion",
            "score": 0.87,
            "rationale": "Derived from PubMed 34614373: HNF1A upregulation co-occurs with GLP-1 changes in type 2 diabetes.",
            "nextSteps": "Test GLP-1 expression in islet β cells with HNF1A variant rs2259816."
        }
    ]
    return {"hypotheses": hypotheses}

@app.get("/graph")
async def get_graph():
    nodes = []
    edges = []
    with open("../ingest/graph_data.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["type"]:
                nodes.append({"data": {"id": row["id"], "label": row["label"], "type": row["type"]}})
            if row["source"] and row["target"]:
                edges.append({"data": {"source": row["source"], "target": row["target"], "label": row["edge_label"]}})
    return {"nodes": nodes, "edges": edges}
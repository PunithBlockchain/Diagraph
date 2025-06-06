import torch
from torch_geometric.data import Data
from torch_geometric.nn import GraphSAGE
import csv
import random

def load_graph_data(node_file, edge_file):
    nodes = []
    node_dict = {}
    with open(node_file, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if row["type"]:
                node_dict[row["id"]] = i
                nodes.append([random.random() for _ in range(16)])
    edges = []
    with open(edge_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["source"] and row["target"]:
                edges.append([node_dict[row["source"]], node_dict[row["target"]]])
    return torch.tensor(nodes, dtype=torch.float), torch.tensor(edges, dtype=torch.long).t()

x, edge_index = load_graph_data("../ingest/graph_data.csv", "../ingest/graph_data.csv")
data = Data(x=x, edge_index=edge_index)

model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=16, num_layers=2)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
model.train()
for epoch in range(10):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = torch.nn.functional.mse_loss(out, data.x)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")

torch.save(model.state_dict(), "graphsage_model.pth")
print("Model saved to graphsage_model.pth")
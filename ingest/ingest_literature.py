from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import requests
from bs4 import BeautifulSoup
import csv
import hashlib
import subprocess
import json

# Load BioBERT for NER
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
model = AutoModelForTokenClassification.from_pretrained("dmis-lab/biobert-v1.1")
ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def fetch_pubmed_abstract(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=text&rettype=abstract"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(strip=True)
        # Log to Solana
        data_hash = hashlib.sha256(text.encode()).hexdigest()
        log_to_solana({"source": "PubMed", "id": pmid, "hash": data_hash})
        return text
    except Exception as e:
        print(f"Error fetching PMID {pmid}: {e}")
        return None

def fetch_clinical_trial(nct_id):
    url = f"https://clinicaltrials.gov/api/query/study_fields?expr={nct_id}&fields=NCTId,BriefTitle,Condition,InterventionName&fmt=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        study = data.get("StudyFieldsResponse", {}).get("StudyFields", [{}])[0]
        trial_data = {
            "id": study.get("NCTId", ""),
            "title": study.get("BriefTitle", ""),
            "condition": study.get("Condition", []),
            "intervention": study.get("InterventionName", [])
        }
        # Log to Solana
        data_hash = hashlib.sha256(json.dumps(trial_data).encode()).hexdigest()
        log_to_solana({"source": "ClinicalTrials", "id": nct_id, "hash": data_hash})
        return trial_data
    except Exception as e:
        print(f"Error fetching NCT {nct_id}: {e}")
        return None

def log_to_solana(data):
    """Call Solana client to log data provenance."""
    try:
        with open("temp_data.json", "w") as f:
            json.dump(data, f)
        subprocess.run(["python", "../blockchain/client/log_data.py", "temp_data.json"], check=True)
        print(f"Logged to Solana: {data}")
    except Exception as e:
        print(f"Error logging to Solana: {e}")

def extract_entities(text):
    if not text:
        return []
    entities = ner(text)
    return [{"entity": ent['word'], "type": ent['entity_group'], "score": ent['score']} for ent in entities]

def save_to_csv(nodes, edges, filename="graph_data.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["type", "id", "label", "source", "target", "edge_label"])
        for node in nodes:
            writer.writerow([node["type"], node["id"], node["label"], "", "", ""])
        for edge in edges:
            writer.writerow(["", "", "", edge["source"], edge["target"], edge["label"]])

if __name__ == "__main__":
    nodes = []
    edges = []
    # Fetch PubMed paper (PMID 34614373)
    abstract = fetch_pubmed_abstract("34614373")
    if abstract:
        entities = extract_entities(abstract)
        for i, ent in enumerate(entities):
            if ent["score"] > 0.7:
                node_type = "Gene" if "gene" in ent["type"].lower() else "Biomarker" if "bio" in ent["type"].lower() else "Other"
                nodes.append({"type": node_type, "id": f"n{i}", "label": ent["entity"]})
        if len(nodes) > 1:
            edges.append({"source": nodes[0]["id"], "target": nodes[1]["id"], "label": "ASSOCIATED_WITH"})
        print("PubMed Entities:", entities)

    # Fetch ClinicalTrials trial (NCT04255433)
    trial = fetch_clinical_trial("NCT04255433")
    if trial:
        nodes.append({"type": "ClinicalTrial", "id": trial["id"], "label": trial["title"]})
        for condition in trial["condition"]:
            nodes.append({"type": "Disease", "id": f"d{len(nodes)}", "label": condition})
            edges.append({"source": trial["id"], "target": f"d{len(nodes)-1}", "label": "STUDIES"})
        for intervention in trial["intervention"]:
            nodes.append({"type": "Drug", "id": f"i{len(nodes)}", "label": intervention})
            edges.append({"source": trial["id"], "target": f"i{len(nodes)-1}", "label": "TESTS"})
        print("Trial Data:", trial)

    save_to_csv(nodes, edges)
    print("Data saved to graph_data.csv")
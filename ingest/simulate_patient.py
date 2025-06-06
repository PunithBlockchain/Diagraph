import csv
import random
import hashlib
import json
import subprocess

def simulate_patient_data(num_records=5, filename="patient_data.csv"):
    headers = ["id", "age", "bmi", "hba1c", "glucose", "population"]
    data = []
    for i in range(num_records):
        record = {
            "id": f"p{i}",
            "age": random.randint(20, 60),
            "bmi": round(random.uniform(18.5, 35.0), 1),
            "hba1c": round(random.uniform(5.0, 10.0), 1),
            "glucose": random.randint(70, 200),
            "population": random.choice(["South Asian", "Caucasian", "African"])
        }
        data.append(record)
        # Log to Solana
        data_hash = hashlib.sha256(json.dumps(record).encode()).hexdigest()
        log_to_solana({"source": "PatientSim", "id": record["id"], "hash": data_hash})
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow([row["id"], row["age"], row["bmi"], row["hba1c"], row["glucose"], row["population"]])
    print(f"Simulated patient data saved to {filename}")

def log_to_solana(data):
    try:
        with open("temp_data.json", "w") as f:
            json.dump(data, f)
        subprocess.run(["python", "../blockchain/client/log_data.py", "temp_data.json"], check=True)
        print(f"Logged to Solana: {data}")
    except Exception as e:
        print(f"Error logging to Solana: {e}")

if __name__ == "__main__":
    simulate_patient_data()
from neo4j import GraphDatabase
import csv
import sys
from pathlib import Path

class GraphImporter:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print(f"Error connecting to Neo4j: {e}")
            sys.exit(1)

    def close(self):
        try:
            self.driver.close()
        except Exception as e:
            print(f"Error closing Neo4j connection: {e}")

    def import_data(self, csv_file):
        try:
            csv_path = Path(csv_file)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_file}")

            with self.driver.session() as session:
                with open(csv_path, 'r') as file:
                    reader = csv.DictReader(file)
                    required_keys = {"type", "id", "label", "source", "target", "edge_label"}
                    for row in reader:
                        # Validate row keys
                        if not all(key in row for key in ["id", "label"]):
                            print(f"Skipping row with missing id/label: {row}")
                            continue

                        # Create node if type is provided
                        if row.get("type"):
                            session.run(
                                "MERGE (n:$type {id: $id}) SET n.label = $label",
                                type=row["type"],
                                id=row["id"],
                                label=row["label"]
                            )

                        # Create relationship if source, target, and edge_label are provided
                        if row.get("source") and row.get("target") and row.get("edge_label"):
                            session.run(
                                """
                                MATCH (s {id: $source}), (t {id: $target})
                                MERGE (s)-[r:RELATION {type: $edge_label}]->(t)
                                SET r.label = $label
                                """,
                                source=row["source"],
                                target=row["target"],
                                edge_label=row["edge_label"],
                                label=row.get("edge_label", "")
                            )
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error importing graph data: {e}")

    def import_patient_data(self, csv_file):
        try:
            csv_path = Path(csv_file)
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file not found: {csv_file}")

            with self.driver.session() as session:
                with open(csv_path, 'r') as file:
                    reader = csv.DictReader(file)
                    required_keys = {"id", "age", "bmi", "hba1c", "glucose", "population"}
                    for row in reader:
                        if not all(key in row for key in required_keys):
                            print(f"Skipping row with missing keys: {row}")
                            continue
                        session.run(
                            """
                            MERGE (p:PatientProfile {id: $id})
                            SET p.age = $age, p.bmi = $bmi, p.hba1c = $hba1c,
                                p.glucose = $glucose, p.population = $population
                            """,
                            id=row["id"],
                            age=int(row["age"]),
                            bmi=float(row["bmi"]),
                            hba1c=float(row["hba1c"]),
                            glucose=int(row["glucose"]),
                            population=row["population"]
                        )
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error converting data types: {e}")
        except Exception as e:
            print(f"Error importing patient data: {e}")

if __name__ == "__main__":
    try:
        importer = GraphImporter("bolt://localhost:7687", "neo4j", "password")
        importer.import_data("../ingest/graph_data.csv")
        importer.import_patient_data("../ingest/patient_data.csv")
        importer.close()
        print("Data imported to Neo4j")
    except Exception as e:
        print(f"Main execution error: {e}")
        sys.exit(1)
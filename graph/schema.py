from neo4j import GraphDatabase

class GraphSchema:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def define_schema(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (g:Gene) REQUIRE g.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE g.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Population) REQUIRE p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:ClinicalTrial) REQUIRE c.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) REQUIRE dr.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (pt:PatientProfile) REQUIRE pt.id IS UNIQUE")
            print("Schema constraints defined.")

if __name__ == "__main__":
    schema = GraphSchema("bolt://localhost:7687", "neo4j", "password")
    schema.define_schema()
    schema.close()
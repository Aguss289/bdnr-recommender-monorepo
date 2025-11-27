from neo4j import GraphDatabase
import json

URI = "bolt://localhost:7687"
AUTH = ("neo4j","testpassword")

driver = GraphDatabase.driver(URI, auth=AUTH)

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '../data/seed_users.json')

with open(data_path) as f:
    data = json.load(f)

def create_nodes(tx):
    for u in data["users"]:
        tx.run("MERGE (x:User {id:$id}) SET x.name=$name, x.lang=$lang", id=u["id"], name=u["name"], lang=u["lang"])
    for s in data["skills"]:
        tx.run("MERGE (x:Skill {id:$id}) SET x.name=$name", id=s["id"], name=s["name"])
    for m in data["masters"]:
        tx.run("""
            MATCH (u:User {id:$uid}), (s:Skill {id:$sid})
            MERGE (u)-[r:MASTERS]->(s)
            SET r.score = $score
            """, uid=m["user"], sid=m["skill"], score=m["score"])

with driver.session() as session:
    session.execute_write(create_nodes)

driver.close()
print("Seed cargada.")

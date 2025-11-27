from fastapi import FastAPI
from neo4j import GraphDatabase

app = FastAPI()
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","testpassword"))

@app.get("/")
def root():
    return {"message": "Recommender API is running"}

@app.get("/recommend/{user_id}")
def recommend(user_id: str, limit: int = 5):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {id:$uid})-[r:MASTERS]->(s:Skill)
            WHERE r.score < 0.6
            MATCH (s)-[:ASSESSED_BY]->(e:Exercise)
            RETURN DISTINCT e.id as exercise, e.name as name LIMIT $lim
        """, uid=user_id, lim=limit)
        return [dict(rec) for rec in result]

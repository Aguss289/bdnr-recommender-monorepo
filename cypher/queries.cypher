// 1) Skills débiles de u2
MATCH (u:User {id:'u2'})-[r:MASTERS]->(s:Skill)
WHERE r.score < 0.5
RETURN s.name, r.score ORDER BY r.score ASC;

// 2) Usuarios con skills en común (conteo)
MATCH (u:User {id:'u1'})-[r1:MASTERS]->(s:Skill)<-[r2:MASTERS]-(other:User)
WHERE other.id <> 'u1'
RETURN other.id, count(s) as shared
ORDER BY shared DESC;

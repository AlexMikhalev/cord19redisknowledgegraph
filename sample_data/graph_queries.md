Match (n)-[r]->(m)
Return n,r,m limit 5

Match (n)-[r]->(m) where n.id in ['C5190416', 'C5195989', 'C5105487', 'C4741648']
Return n,r,m limit 5


query="""WITH ['C5190416', 'C5195989', 'C5105487', 'C4741648'] as ids
MATCH (e:entity) where e.id in ids
WITH collect(e) as entities
WITH head(entities) as head, tail(entities) as entities
MATCH (head)-[r:related]->(m)
RETURN head,r,m"""
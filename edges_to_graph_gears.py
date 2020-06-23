def create_node(x):
    source_id, destination_id=x['key'].split(':')[-2:]
    node=x['value']
    edge_string="""
    MATCH (e:entity {id:'%s' }),(t:entity { id: '%s'})
    MERGE (e)-[r:related {rank:%s}]->(t)
    RETURN e.id, type(r), t.id
    """ %(source_id, destination_id,x['value']['rank'])
    # log(f"Node string {edge_string}")
    execute('GRAPH.QUERY', 'CORD19GRAPH', edge_string)

bg = GearsBuilder()
bg.foreach(create_node)
bg.count()
bg.run('edges:*')


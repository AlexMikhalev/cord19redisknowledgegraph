def create_node(x):
    node=x['value']
    node_string="MERGE (%s:entity {id: '%s', name: '%s', rank: '%s'})" % (node['id'], node['id'],node['name'],node['rank'])
    log(f"Node string {node_string}")
    execute('GRAPH.QUERY', 'CORD19GRAPH', node_string)

bg = GearsBuilder()
bg.foreach(create_node)
bg.count()
bg.register('nodes:*')


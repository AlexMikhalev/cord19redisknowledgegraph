import redis
from redisgraph import Node, Edge, Graph, Path

r = redis.Redis(host='10.144.17.211', port=6379)

redis_graph = Graph('social', r)

john = Node(label='person', properties={'name': 'John Doe', 'age': 33, 'gender': 'male', 'status': 'single'})
redis_graph.add_node(john)

japan = Node(label='country', properties={'name': 'Japan'})
redis_graph.add_node(japan)

edge = Edge(john, 'visited', japan, properties={'purpose': 'pleasure'})
redis_graph.add_edge(edge)

redis_graph.commit()
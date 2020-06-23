import redis
import config
from redisgraph import Graph

r = redis.Redis(host=config.config()['host'],port=config.config()['port'])
redis_graph = Graph('CORD19GRAPH', r)

from automata.utils import *

def match_nodes(search_string, Automata=Automata):
    if not Automata:
        Automata=loadAutomata()
    nodes=set()
    matched_ents=find_matches(search_string,Automata)
    nodes = set([node[0] for node in matched_ents])
    return list(nodes)



def get_nodes(nodes):
    node_list=list()
    params = {'ids':nodes}
    query="""WITH $ids as ids 
    MATCH (e:entity) where e.id in ids RETURN DISTINCT e.id,e.name,max(e.rank)"""
    result = redis_graph.query(query, params)
    # result.pretty_print()
    for record in result.result_set:
        node_list.append({'id':record[0],'name':record[1],'rank':record[2]})
    return node_list

def get_edges(nodes):
    links=list()
    params = {'ids':nodes}
    query="""WITH $ids as ids
    MATCH (e:entity)-[r]->(t:entity) where e.id in ids RETURN DISTINCT e.id,t.id,max(r.rank)"""
    result = redis_graph.query(query,params)
    # result.pretty_print()
    for record in result.result_set:
        links.append({'source':record[0],'target':record[1],'rank':record[2]})
    return links


if __name__ == "__main__":
    search_string="How does temperature and humidity affect the transmission of 2019-nCoV?"
    nodes=match_nodes(search_string)
    node_list=get_nodes(nodes)
    links=get_edges(nodes)
    print(node_list)
    print("---")
    print(links)


"""
 This is a candidate for rgsync and/or lua script 
MATCH (e:entity {id:'C4465947' }),(t:entity { id: 'C2603714'})
MERGE (e)-[r:related]->(t)
RETURN e.id, type(r), t.id

MATCH (e:entity {id:'C4465947' }),(t:entity { id: 'C2603714'})
MERGE (e)-[r:related {rank:1}]->(t)
RETURN e.id, type(r), r.rank, t.id


MATCH (e:entity {id:'C4465947' }),(t:entity { id: 'C2603714'})
MERGE (e)-[r:related {rank:1, list_r:[1,3]}]->(t)
RETURN e.id, type(r), r.list_r, t.id

FIXME: Create a relationship from edges_scored and populate list of articles inside relationship

"""

import redis
import config
from common.utils import * 
redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)

if __name__ == "__main__":
    for key in redis_client.scan_iter("edges:*",count=10):
        if redis_client.sismember('processed_edges', key):
            log(f"Already processed edge {key}")
        else:
            edge=redis_client.hgetall(key) 


            node_string="MERGE (%s:entity {id: '%s', name: '%s', rank: '%s'})" % (node['id'], node['id'],node['name'],node['rank'])
            print(node_string) 
            redis_client.execute_command("GRAPH.QUERY", "DEMOGRAPH", node_string, "--compact")
            redis_client.sadd('processed_edges',key)
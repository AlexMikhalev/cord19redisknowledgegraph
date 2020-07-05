"""
 This is a candidate for rgsync and/or lua script 
"""

import redis
import config
from common.utils import * 
redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)

if __name__ == "__main__":
    for key in redis_client.scan_iter("nodes:*",count=10):
        if redis_client.sismember('processed_nodes', key):
            log(f"Already processed node {key}")
        else:
            node=redis_client.hgetall(key) 
            node_string="MERGE (%s:entity {id: '%s', name: '%s', rank: '%s'})" % (node['id'], node['id'],node['name'],node['rank'])
            print(node_string) 
            redis_client.execute_command("GRAPH.QUERY", "DEMOGRAPH", node_string, "--compact")
            node_string="MERGE (n:entity {id: '%s', name: '%s', rank: '%s'})" % ( node['id'], node['name'],node['rank'])
            print(node_string)
            redis_client.sadd('processed_nodes',key)
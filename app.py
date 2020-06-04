#!flask/bin/python
from flask import Flask, jsonify, request,json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from automata.utils import *
import itertools
"""
The purpose of this script is to mimic simple graph processing to support Visualisation/Web development effort. 
Use RedisSearch instead
{ nodes: [ { id : 'aa', name: 'aaa' }, { id: 'bb', name: 'bbbb' }], linkes[{ source: 'aa', target: 'bb']
"""
try:
    import redis
    import config
    redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)
except:
    log("Redis is not available ")

import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])

try:
    from rediscluster import RedisCluster
    rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)
except:
    log("Redis Cluster is not available ")

@app.route('/')
def index():
    return "Sample server, use RedisGraph instead if available"

@app.route('/edge/<edge_string>')
def get_edgeinfo(edge_string):
    """
    Tested with edges:C5162902:C5190121
    """
    log("Edge string "+edge_string)
    edges_query=remove_prefix(edge_string,'edges:')
    result_table=[]
    edge_scored=redis_client.zrangebyscore(f"edges_scored:{edges_query}",'-inf','inf',0,5)
    if edge_scored:
        for sentence_key in edge_scored:
            sentence=rediscluster_client.get(sentence_key)
            article_id=sentence_key.split(':')[1]
            title=rediscluster_client.get(f"title:{article_id}")
        result_table.append({'title':title,'sentence':sentence,'sentencekey':sentence_key})
    else:
        result_table.append(redis_client.hgetall(f'{edge_string}'))
    
    return jsonify({'results': result_table}), 200

@app.route('/search', methods=['POST'])
def create_task():
    if not request.json or not 'search' in request.json:
        abort(400)
    search_string=request.json['search']
    matched_ents=find_matches(search_string,Automata)
    nodes=[]
    links=[]
    for pair in itertools.combinations(matched_ents, 2):
        source_entity_id=pair[0][0]
        destination_entity_id=pair[1][0]
        edge_call=redis_client.hgetall(f'edges:{source_entity_id}:{destination_entity_id}')
        edge={'source':source_entity_id,'target':destination_entity_id}
        if edge_call:
            log("Edge call"+str(edge_call))
            links.append(edge)
        else:
            #FIXME: made up for demo: always returns link even if it doesn't exists.
            links.append(edge)
        
        source_node=redis_client.hgetall(f'nodes:{source_entity_id}')
        if source_node:
            nodes.append(source_node)
        else:
            nodes.append({'id':source_entity_id,'name':source_entity_id})
        destination_node=redis_client.hgetall(f'nodes:{destination_entity_id}')
        if destination_node:
            nodes.append(destination_node)
        else:
            nodes.append({'id':destination_entity_id,'name':destination_entity_id})

    search_result={
        'nodes': nodes,
        'links': links
    }
    return jsonify({'search_result': search_result}), 200

if __name__ == "__main__":
    app.run(port=8181, host='10.144.17.211')


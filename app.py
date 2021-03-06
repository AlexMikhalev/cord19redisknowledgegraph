#!flask/bin/python
from flask import Flask, jsonify, request,json, abort
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

from graphsearch.graph_search import * 

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
    log("Result table "+str(result_table))
    if result_table==[{}]:
        abort(404)
    else:
        #FIXME: this tuple conversion doesn't make sense
        return jsonify(tuple(result_table)), 200
    
@app.route('/search', methods=['POST'])
def search_task():
    if not request.json or not 'search' in request.json:
        abort(400)
    search_string=request.json['search']
    matched_ents=find_matches(search_string,Automata)
    nodes=[]
    nodes_set=set()
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
        if source_entity_id not in nodes_set:
            source_node=redis_client.hgetall(f'nodes:{source_entity_id}')
            if source_node:
                nodes.append(source_node)
            else:
                nodes.append({'id':source_entity_id,'name':source_entity_id})
            nodes_set.add(source_entity_id)
        if destination_entity_id not in nodes_set:    
            destination_node=redis_client.hgetall(f'nodes:{destination_entity_id}')
            if destination_node:
                nodes.append(destination_node)
            else:
                nodes.append({'id':destination_entity_id,'name':destination_entity_id})
            nodes_set.add(destination_entity_id)

    return jsonify({'nodes': nodes,'links': links}), 200



from qasearch.qa_bert import *

@app.route('/gsearch', methods=['POST'])
def gsearch_task():
    """
    this search using Redis Graph to get list of nodes and links
    """
    if not request.json or not 'search' in request.json:
        abort(400)
    search_string=request.json['search']

    nodes=match_nodes(search_string)
    links,node_list=get_edges(nodes)
    node_list=get_nodes(node_list)
    return jsonify({'nodes': node_list,'links': links}), 200

@app.route('/qasearch', methods=['POST'])
def qasearch_task():
    """
    this search using Redis Graph to get list of articles and sentences and then calls BERT QA model to create answer
    This is ugly draft to prove the point. 
    TODO: pre-process articles with qa tokeniser 
    TODO: pre-process article create hash with article_id, title and content
    TODO: apply spellcheck to all articles titles and content
    """
     

    if not request.json or not 'search' in request.json:
        abort(400)
    question=request.json['search']
    nodes=match_nodes(question)
    links,node_list=get_edges_limited(nodes)
    result_table=[]
    for each_record in links:  
        edge_query=each_record['source']+":"+each_record['target'] 
        print(edge_query)
        edge_scored=redis_client.zrangebyscore(f"edges_scored:{edge_query}",'-inf','inf',0,5)
        if edge_scored:
            for sentence_key in edge_scored:
                sentence=rediscluster_client.get(sentence_key)
                article_id=sentence_key.split(':')[1]
                title=rediscluster_client.get(f"title:{article_id}")
                article_content=rediscluster_client.get(f"paragraphs:{article_id}")
                answer=qa(question,sentence)
            result_table.append({'title':title,'sentence':sentence,'sentencekey':sentence_key,'answer':answer})        

    return jsonify({'links': links,'results':result_table}), 200



if __name__ == "__main__":
    app.run(port=8181, host='10.144.17.211')


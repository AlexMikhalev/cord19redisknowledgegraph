
import ujson as json
from redis.exceptions import ResponseError
from rediscluster import RedisCluster
from redisbloom.client import Client



import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])
redisbloomclient = Client(host=config.config()['host'],port=config.config()['port'])


rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)
import redis
rediscluster_client = redis.Redis(host=config.config()['host'],port=config.config()['port'])


import os
from concurrent.futures import ThreadPoolExecutor, as_completed
n_cpus = os.cpu_count()
print(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)

from pathlib import Path


datapath = Path('../input')


def parse_json_body_text(json_filename):
    print("Processing ..", json_filename.stem)
    with open(json_filename) as json_data:
        data = json.load(json_data)
        for body_text in data['body_text']:
            para = body_text['text']
            yield para

#process document return sentences and entities 
def process_file(f, rediscluster_client=rediscluster_client):
    article_id=f.stem
    print("Processing article_id ", article_id)
    if rediscluster_client.sismember('processed_docs_stage1_para', article_id):
        print("already processed ", article_id)
        return article_id
    article_body=[]
    for para in parse_json_body_text(f):
        article_body.append(para)
    rediscluster_client.set(f"paragraphs:{article_id}"," ".join(article_body))
    rediscluster_client.sadd('processed_docs_stage1_para',article_id) 
    return article_id

# main submission loop 
counter=0
processed=[]
json_filenames = datapath.glob('**/*.json')
for each_file in json_filenames:
    print("Submitting task")
    task=executor.submit(process_file,each_file,rediscluster_client)
    processed.append(task)
    counter+=1
    if counter>200:
        break

    
print("Waiting for tasks to complete")
for each_task in as_completed(processed):
    print(task.result())
print("Completed")





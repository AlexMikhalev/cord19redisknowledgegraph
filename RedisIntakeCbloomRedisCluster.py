
import ujson as json
from redis.exceptions import ResponseError
from rediscluster import RedisCluster
from redisbloom.client import Client



import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])
redisbloomclient = Client(host=config.config()['host'],port=config.config()['port'])


rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)

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
        paper_id=data['paper_id']
        for body_text in data['body_text']:
            para = body_text['text']
            yield para


try:
    redisbloomclient.cfCreate('processed_documents', 40000)
except ResponseError as e:
    print("Error:", repr(e))


#process document return sentences and entities 
def process_file(f,redisbloomclient=redisbloomclient, rediscluster_client=rediscluster_client):
    pid = 0
    article_id=f.stem
    print("Processing article_id ", article_id)
    if redisbloomclient.cfExists('processed_documents', article_id):
        print("already processed ", article_id)
        return article_id
    for para in parse_json_body_text(f):
        rediscluster_client.setnx(f"paragraphs:{article_id}:pid:{pid}",para)
        pid+= 1
    redisbloomclient.cfAdd('processed_documents', article_id) 
    return article_id

# main submission loop 
processed=[]
json_filenames = datapath.glob('**/*.json')
for each_file in json_filenames:
    print("Submitting task")
    task=executor.submit(process_file,each_file,redisbloomclient,rediscluster_client)
    processed.append(task)
    
print("Waiting for tasks to complete")
for each_task in as_completed(processed):
    print(task.result())
print("Completed")





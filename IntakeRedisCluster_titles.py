
import ujson as json
from redis.exceptions import ResponseError

from rediscluster import RedisCluster


import sys
from datetime import datetime
from pathlib import Path
LOG_PATH = Path('./logs/')
LOG_PATH.mkdir(exist_ok=True)

import logging
run_start_time = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
logfile = str(LOG_PATH/'log-{}-{}.txt'.format(run_start_time, "Parsing headers"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout)
    ])

logger = logging.getLogger()


import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])
rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)


import os
from concurrent.futures import ThreadPoolExecutor, as_completed
n_cpus = os.cpu_count()
logger.info(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)

from pathlib import Path


datapath = Path('../input')

setname='processed_docs_stage1_title'

def parse_json_title(json_filename):
    logging.info("Processing ..", json_filename.stem)
    with open(json_filename) as json_data:
        data = json.load(json_data)
        return str(data['metadata']['title'])

#process document return sentences and entities 
def process_file(f, rediscluster_client=rediscluster_client):
    article_id=f.stem
    logger.info("Processing article_id ", article_id)
    if rediscluster_client.sismember(setname, article_id):
        logger.info("already processed ", article_id)
        return article_id
    article_title=parse_json_title(f)
    rediscluster_client.set(f"title:{article_id}",article_title)
    rediscluster_client.sadd(setname,article_id) 
    return article_id

# main submission loop 
processed=[]
counter=0
start_time=datetime.now()
json_filenames = datapath.glob('**/*.json')
for each_file in json_filenames:
    logger.info("Submitting task")
    task=executor.submit(process_file,each_file,rediscluster_client)
    processed.append(task)


    
logger.info("Waiting for tasks to complete")
for each_task in as_completed(processed):
    logger.info(task.result())
logger.info("Completed in: {:s}".format(str(datetime.now()-start_time)))




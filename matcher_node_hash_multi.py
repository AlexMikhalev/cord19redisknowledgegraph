#FIXME create a string based tokens 
#TODO: amend next step to take strings as input instead of list
import ujson as json

import redis

from redis.exceptions import ResponseError
from rediscluster import RedisCluster

import re



import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])

rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)
redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)

from automata.utils import * 
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import itertools
from common.utils import * 

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
n_cpus = os.cpu_count()
logger.info(f'Number of CPUs: {n_cpus}')
executor = ThreadPoolExecutor(max_workers=n_cpus)


if __name__ == "__main__":
    """
    This is matcher node hash: it builds a hash structure in Redis with aim to prepare for 
    RedisGraph population 
    """
    Automata=loadAutomata()

    num_sents = 0 
    all_lists_processed=rediscluster_client.keys('processed_docs_stage3_tokenized*')
    # all_lists_processed=rediscluster_client.keys('processed_docs_stage3_tokenized{1x3}')

    def process_item(sentence_list_key, Automata, rediscluster_client, redis_client):
        sentences_list=rediscluster_client.smembers(sentence_list_key)
        for item in sentences_list:
            # TODO: make sure it works
            tokens=set(rediscluster_client.get(item).split(' '))
            tokens.difference_update(STOP_WORDS)
            tokens.difference_update(set(punctuation)) 
            matched_ents = find_matches(" ".join(tokens), Automata)
            if len(matched_ents)<1:
                log("Error matching sentence "+item)
            else:
                for pair in itertools.combinations(matched_ents, 2):
                    source_entity_id=pair[0][0]
                    destination_entity_id=pair[1][0]
                    sentence_key=":".join(item.split(':')[2:-1])
                    label_source=redis_client.get(source_entity_id)
                    label_destination=redis_client.get(destination_entity_id)

                    if not label_source:
                        label_source=pair[0][1]

                    if not label_destination:
                        label_destination=pair[1][1]
                    #FIXME: seems spaces are ok in names for Graph Labels
                    source_canonical_name=re.sub('[^A-Za-z0-9]+', ' ', str(label_source))
                    destination_canonical_name=re.sub('[^A-Za-z0-9]+', ' ', str(label_destination))

                    redis_client.hsetnx(f'nodes:{source_entity_id}','id',source_entity_id)
                    redis_client.hsetnx(f'nodes:{source_entity_id}','name',source_canonical_name)
                    redis_client.hsetnx(f'nodes:{destination_entity_id}','id',destination_entity_id)
                    redis_client.hsetnx(f'nodes:{destination_entity_id}','name',destination_canonical_name)
                    redis_client.hincrby(f'nodes:{source_entity_id}' ,'rank',1)
                    redis_client.hincrby(f'nodes:{destination_entity_id}','rank',1)
                    redis_client.zincrby(f'edges_scored:{source_entity_id}:{destination_entity_id}',1, sentence_key)
                    redis_client.hincrby(f'edges:{source_entity_id}:{destination_entity_id}','rank',1)
            #Delete processed sentence to avoid re-processing (Use Streams instead)
            log(f"Processed item {item}")
            rediscluster_client.srem(sentence_list_key,item)

    # main submission loop 
    counter=0 
    processed=[]
    for each_item in all_lists_processed:
        logger.info("Submitting task")
        task=executor.submit(process_item, each_item, Automata, rediscluster_client, redis_client)
        processed.append(task)
        counter+=1
        if counter>200:
            break

    logger.info("Waiting for tasks to complete")
    for each_task in as_completed(processed):
        if num_sents % 100 == 0:
            log(f"... {num_sents} sentences ")
        logger.info(task.result())
        num_sents+=1

    logger.info("Completed")
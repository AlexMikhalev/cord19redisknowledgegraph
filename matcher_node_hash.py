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

import ahocorasick 
import joblib
import itertools
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from common.utils import * 


def loadAutomata():
    from urllib.request import urlopen
    import ahocorasick 
    import joblib
    # Automata=joblib.load(urlopen("https://github.com/AlexMikhalev/cord19redisknowledgegraph/raw/master/automata/automata_syns.pkl.bz2"))
    Automata=joblib.load("./automata/automata_syns.pkl.bz2")
    log("Automata properties" + str(Automata.get_stats()))
    return Automata

def find_matches(sent_text, A):
    matched_ents = []
    for char_end, (eid, ent_text) in A.iter(sent_text):
        char_start = char_end - len(ent_text)
        matched_ents.append((eid, ent_text, char_start, char_end))
    # remove shorter subsumed matches
    longest_matched_ents = []
    for matched_ent in sorted(matched_ents, key=lambda x: len(x[1]), reverse=True):
        longest_match_exists = False
        char_start, char_end = matched_ent[2], matched_ent[3]
        for _, _, ref_start, ref_end in longest_matched_ents:
            if ref_start <= char_start and ref_end >= char_end:
                longest_match_exists = True
                break
        if not longest_match_exists:
            # print("adding match to longest")
            longest_matched_ents.append(matched_ent)
    return [t for t in longest_matched_ents if len(t[1])>3] 

if __name__ == "__main__":
    """
    This is matcher node hash: it builds a hash structure in Redis with aim to prepare for 
    RedisGraph population 
    """
    Automata=loadAutomata()

    num_sents = 0 
    all_lists_processed=rediscluster_client.keys('processed_docs_stage3_tokenized*')
    # all_lists_processed=rediscluster_client.keys('processed_docs_stage3_tokenized{1x3}')

    for each_item in all_lists_processed:
        sentences_list=rediscluster_client.smembers(each_item)
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
            rediscluster_client.srem(each_item,item)
            if num_sents % 100 == 0:
                log(f"... {num_sents} sentences ")
            num_sents+=1
            # log("Finished graph for sentence %s " % sentence_key)

    logger.info("Completed")
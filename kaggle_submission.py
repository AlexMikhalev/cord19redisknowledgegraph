import json 
import itertools
import os 
from automata.utils import *
import redis
import config
redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)
import config
rc_list=json.loads(config.config(section='rediscluster')['rediscluster'])
from rediscluster import RedisCluster
rediscluster_client = RedisCluster(startup_nodes=rc_list, decode_responses=True)
import re 

list_of_relevant_factors=["Effectiveness of case isolation/isolation of exposed individuals (i.e. quarantine)",
"Effectiveness of community contact reduction",
"Effectiveness of inter/inner travel restriction",
"Effectiveness of school distancing",
"Effectiveness of workplace distancing",
"Effectiveness of a multifactorial strategy prevent secondary transmission",
"Seasonality of transmission",
"How does temperature and humidity affect the transmission of 2019-nCoV?",
"Significant changes in transmissibility in changing seasons?",
"Effectiveness of personal protective equipment (PPE)"]

for each_factor in list_of_relevant_factors:
    print(f"{each_factor}")
    result_table=[]
    file_name=re.sub('[^A-Za-z0-9]+', '_', str(each_factor))
    fout = open( "./data/"+str(file_name)+".tsv", "w") 
    matched_ents=find_matches(each_factor,Automata)
    for pair in itertools.combinations(matched_ents, 2):
        source_entity_id=pair[0][0]
        destination_entity_id=pair[1][0]
        # print(f"edges:{source_entity_id}:{destination_entity_id}")
        edge_scored=redis_client.zrangebyscore(f"edges_scored:{source_entity_id}:{destination_entity_id}",0,'inf',0,5)
        if edge_scored:
            for sentence_key in edge_scored:
                sentence=rediscluster_client.get(sentence_key)
                article_id=sentence_key.split(':')[1]
                # print(article_id)
                title=rediscluster_client.get(f"title:{article_id}")
                # print(title)
                if title:
                    result_table.append({'Study':title,'Excerpt':sentence})
                    fout.write("{:s}|{:s}\n".format(title, sentence))
        
    print(result_table)
    fout.close()
    print("-----")
            
#!/usr/bin/env python
# coding: utf-8

# In[2]:


from utils_for_automata import * 
import itertools

import re


# FIXME: for this to work automata should return formal concept name  when 
# matching sentences ./kaggle/working/automata_ent_syn.pkl is default
# FIXME check with ./kaggle/working/automata_ent_only.pkl - may be better matching to entities only


print("Loading Aho Corasic Automata")
A=joblib.load("./kaggle/working/automata_ent_only.pkl")
print("Automata properties")
print(A.get_stats())

import asyncio
import aioredis


async def main():
    num_sents, num_ents = 0, 0
    session = Session(engine)
    redis = await aioredis.create_redis_pool('redis://localhost')
    for sdoc in session.query(Sentences).yield_per(400).enable_eagerloads(False):
        if num_sents % 100 == 0:
            print("... {:d} sentences read, {:d} entities written"
                    .format(num_sents, num_ents))
        matched_ents = find_matches(str(sdoc.sentence_tokenised), A)
        if len(matched_ents)<1:
            print("Error ", sdoc.sentence_tokenised)
        else:
            for pair in itertools.combinations(matched_ents, 2): 
                source_canonical_name=re.sub('[^A-Za-z0-9]+', '_', str(pair[0][1]))
                source_entity_id=str(pair[0][0])
                destination_canonical_name=re.sub('[^A-Za-z0-9]+', '_', str(pair[1][1]))
                destination_entity_id=str(pair[1][0])
                sentence_key="{:s}:{:d}:{:d}".format(sdoc.article_id, sdoc.paragraph_id,sdoc.sentence_id)
                await redis.hmset_dict("nodes:{:s}".format(source_entity_id), id=source_entity_id,name=source_canonical_name)
                await redis.hmset_dict("nodes:{:s}".format(destination_entity_id), id=destination_entity_id, name=destination_canonical_name )
                await redis.hmset_dict("edges:{:s}:{:s}:{:s}".format(sentence_key,source_entity_id,destination_entity_id),source_entity_id=source_entity_id, destination_entity_id=destination_entity_id, sentence_key=sentence_key)
                num_ents += 1
        num_sents += 1
    session.close()
    print("Waiting for connections close")
    await redis.bgsave()
    redis.close()
    await redis.wait_closed()
    print("Complete")

asyncio.run(main())





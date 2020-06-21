"""
 This is a candidate for rgsync and/or lua script 
"""

import redis
import config
from common.utils import * 
redis_client = redis.Redis(host=config.config()['host'],port=config.config()['port'],charset="utf-8", decode_responses=True)

if __name__ == "__main__":
    counter=0
    for key in redis_client.scan_iter("edges:*",count=10):
        node=redis_client.hgetall(key)
        print(node) 
        node_dump=redis_client.dump(key)
        counter+=1
        if counter>225:
            break
        test_key="test:"+key
        print(test_key)
        redis_client.restore(test_key,0,node_dump,replace=True)
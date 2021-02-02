SECONDS=0
python RedisIntakeRedisClusterSample.py 
echo "RedisIntakeRedisClusterSample.py finished in $SECONDS seconds."
SECONDS=0
python matcher_node_hash.py 
echo "matcher_node_hash.py finished in $SECONDS seconds."
SECONDS=0
python matcher_node.py 
echo "matcher_node.py finished in $SECONDS seconds."

# cord19redisknowledgegraph
This is a repo to build Knowledge Graph out of CORD19 kaggle data using Redis

This is a next phase of [original Kaggle submission](https://medium.com/@alex.mikhalev/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd)

[Redis 'Beyond Cache' Hackathon Submission](https://devpost.com/software/yggdrasil-covid19-redis-knowledge-graph)

[Submission Summary](./submissionredishack.md)

[Todo](./Roadmap.md)

# Installation 
```
mkdir ./input
pip install kaggle 
cd input
kaggle datasets download allen-institute-for-ai/CORD-19-research-challenge
unzip CORD-19-research-challenge.zip
docker run -d --name rgcluster -p 30001:30001 -p 30002:30002 -p 30003:30003 redislabs/rgcluster:latest
git clone https://github.com/AlexMikhalev/cord19redisknowledgegraph 
cd cord19redisknowledgegraph
pip install gears-cli
sh cluster_pipeline_events.sh
```
# Start Redis Gears cluster
```
docker run -d -v $PWD/conf/docker-config.sh:/cluster/config.sh --name rgcluster -p 30001:30001 -p 30002:30002 -p 30003:30003 redislabs/rgcluster:latest
```
# Rebuild Manually using create-cluster
```
./create-cluster clean
./create-cluster start
 echo "yes" | ./create-cluster create
 redis-trib.py execute --addr 10.144.17.211:30001 RG.REFRESHCLUSTER
 redis-trib.py execute --addr 10.144.17.211:30001 RG.CONFIGSET ExecutionMaxIdleTime 300000
 redis-trib.py execute --addr 10.144.17.211:30001 CONFIG SET proto-max-bulk-len 2048mb
 ```
 



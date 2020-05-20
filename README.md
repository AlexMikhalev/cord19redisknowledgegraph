# cord19redisknowledgegraph
This is a repo to build Knowledge Graph out of CORD19 kaggle data using Redis

This is a next phase of [original Kaggle submission](https://medium.com/@alex.mikhalev/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd)

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
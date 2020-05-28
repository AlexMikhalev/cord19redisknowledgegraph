# Vision 
* Search or rather information exploration should be spacial preferably in VR (memory palace, see Theatre of Giulio Camillo). A force-directed graph is a path towards it, where visual assisted by text — relevant text pops up on the connection and where people explore the concepts and then dig deeper into text.
* When I am exploring topics on science or engineering, I look at the diversity of the opinion, not the variety of the same cluster of words, same thought. I want to avoid confirmation bias. I want to find articles relevant to the same concept, not necessary the ones which have similar words.

# Mission 

To build a natural language processing pipeline, capable of handling a large number of documents and concepts, incorporating System 1 AI (fast, intuitive reasoning) and System 2 (high-level reasoning) and then present knowledge in a modern VR/AR visualisation. Knowledge should be re-usable and shareable. 

# Goal 
Build NLP pipeline leveraging Redis ecosystem whenever possible. We use COVID 19 (CORD19) medical articles corpus as input and experience of participation in the Kaggle CORD19 concept. My major challenge of CORD19 competition was running out of memory/storage and loosing processed steps, building and re-loading snapshots while leveraging modern frameworks like spacy/pytorch. Overall I missed about a week in the competition by re-processing the data. Hence this implementation designed to avoid running out of memory, taking baby steps initially.

# Implementation 

* Ingest documents: RedisIntakeRedisCluster.py parses documents taking out body_text and saves under paragraphs:{article_id} in Redis cluster. Why the redis cluster needed? From experience on Kaggle, I know single instance Redis Server will run out of memory. Nothing fancy, ingest works fast.

*  Detect language: lang_detect_gears_paragraphs.py. Uses Redis Gears by registering key reader on 'paragraphs:*'. One of the surprises in the challenge was that not all medical literature was in English. 

*  Split paragraphs into sentences: spacy_sentences_geared.py. This is where the process becomes interesting; I wanted to use spacy and intelligent parser spacy provides, without the penalty for memory and time required to process. I disabled NER and Tagging components en_core_web_sm.load(disable=['ner','tagger']). With the help of Meir Shpilraien from RedisLabs script evolved into symspell_sentences_streamed.py - using streams to process articles.

* symspell_sentences_streamed.py As I noticed most of the articles are OCR scans, not even spellchecked. Before tokenising, I wanted to make sure it's spellchecked. The script uses symspell library and Redis Gears and stream reader. 

* Process sentences into tokens: tokenizer_bert_stream.py. The step uses transformers BERT based tokeniser specifically adapted to clinical research Bio_ClinicalBERT. It also uses streams as I found them being more reliable than key readers. The deployment was tricky: while RedisLabs strives towards exceptional standards in engineering (Redis Cluster node with Gears takes 6MB RAM), the rest of the industry makes different assumptions about storage/memory available. Again with the help of Meir Shpilraien, we managed to get it working, and there is a ticket in GitHub with discussion. In the end, it worked brilliantly (fast). BERT based tokenisation allows two path - one is via strings matching, where tokens processed as strings, and another (to be explored) where tokens converted to ids and used to feed other ML model like BART for article summarisation. While each of those steps are small and may not look nessesary useful, same pre-processing using Spacy and scispacy raised two challenges: both spacy and scispacy are memory hungry: 9GB RAM on load and processing requires dedicated hardware and a lot of time. Those set of scripts run on commodity server (s) in the background and distribute compute and memory keys evenly. My dream is not to lose data during processing. See demo video. 

*  Prepare Methathesaurus (UMLS): UMLS was loaded into MySQL following UMLS instruction (see sql_import/README.MD and loaded into Redis sql_import/cui_term.sql. While it took time to understand data model, the overall experience of mapping UMLS into Redis was pretty flawless - I could have avoided MySQL use.   

* Build Aho-Corasick aho_corasick_intake.py This script takes the dump of words to Concept Unique Identifiers (CUI). Aho-Corasik is a superb algorithm for this task. It takes a few minutes to run on all medical terms and their variations as per UMLS and output 30 MB Automata (bziped) 

* Matcher: This matcher_node.py script breaks architectural pattern to use Gears/Streams and SHF type of collection. The purpose: we now have a set of tokens, automata to match them into concepts and Redis Graph to be populated with concepts (Nodes) and their relationship (articles).
Each relationship corresponds to the article as they were formed by matching relevant terms from articles into the corresponding edge. This simple step allows to create an information/knowledge dimension: we can create nodes (terms) and relationship (set of articles), but because nodes use industry standard ontology, they can be leveraged by different graphs and different visualisation techniques, it is now possible to build different visualisation on top of it: i.e. if you want to find an articles relevant to body part or medical condition ("bleeding") it is now possible using just traversal of graph database using Cyther. Obviously, it is now also possible to find most important concepts using PageRank algorithm `GRAPH.QUERY cord19medical "CALL algo.pageRank('entity','related')"`. Why use matcher instead of RedisSearch? Initially, I didn't know about the integration of RedisSearch/RedisGraph, it's something to be explored and exploited, while RedisSearch state of the art in the search industry based on different concepts and assumptions to the one I needed. 

* API server: app.py This server build to help support Visualisation development for Brian, it mimics the behaviour of Redis Graphs (in parts I need) and have two APIs /search and /edge. Search API returns nodes and links and edge API fetches all necessary information about article relevant to the link (edge). It's powered by Redis (local), and matcher_node_hash.py builds necessary data structures (without populating them in RedisGraph). Further work would be to map those into RedisGraph: at the moment matcher_node.py hammers RedisGraph and is trying to create node/relationship even if it already exists. matcher_node_hash only create Redis structures. 
* Visualisation: @mcwachanga created a Angular 3D based visualisation using force-directed graphs with potential support for AR/VR, lives in separate branch https://github.com/AlexMikhalev/cord19redisknowledgegraph/tree/phase3

# Conclusion and lessons learned
We took OCR scans in JSON format and turned them into Knowledge Graph, demonstrating how you can apply modern techniques like BERT tokenisation and more traditional Semantic Network/OWL/Methathesaurus technique based on Unified Medical Language System. Redis Ecosystem offers a lot to the data science community, and I hope it will take its place at the core of Kaggle notebooks, ML frameworks and make them more deployable. The success of our industry depends on how our tools work together  - regardless of whether they are engineering, data science, machine learning and organisational or architectural.  

PS. Building a distributed system, even as simple one as this one with kids around is "difficult/funny". Special thank you to my patient wife, Karine.

# Further steps 
* Documentation 
* Make tokeniser useful 
* Make matcher multi-thread/multi process
* Use Write behind pattern to write into Redis Graph 
* Visualisation expansions

```
gears-cli --host 10.144.17.211 --port 30001 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt
SECONDS=0
gears-cli --host 10.144.17.211 --port 30001 symspell_sentences_streamed.py --requirements requirements_gears_symspell.txt
echo "symspell_sentences_streamed.py registered in $SECONDS seconds."
SECONDS=0
gears-cli --host 10.144.17.211 --port 30001 spacy_sentences_streams.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_streams.py registered in $SECONDS seconds."
SECONDS=0
gears-cli --host 10.144.17.211 --port 30001 tokenizer_bert_stream.py --requirements requirements_tokenizer.txt 
echo "tokenizer_bert_stream.py registered in $SECONDS seconds."
sleep 10
SECONDS=0
python RedisIntakeRedisClusterSample.py 
echo "RedisIntakeRedisClusterSample.py finished in $SECONDS seconds."
SECONDS=0
python matcher_node_hash.py 
echo "matcher_node_hash.py finished in $SECONDS seconds."
SECONDS=0
python matcher_node.py 
echo "matcher_node.py finished in $SECONDS seconds."
```

Ways to test search:
```
curl -i -H "Content-Type: application/json" -X POST -d {"""search""":"""SARS Hypothesis Generation family"""} "http://10.144.17.211:8181/search"
```
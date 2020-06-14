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

# SECONDS=0
# python matcher_node_hash.py 
# echo "matcher_node_hash.py finished in $SECONDS seconds."
# SECONDS=0
# python matcher_node.py 
# echo "matcher_node.py finished in $SECONDS seconds."
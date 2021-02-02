gears-cli --host 10.144.17.211 --port 6379 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt

SECONDS=0
gears-cli --host 10.144.17.211 --port 6379 spacy_sentences_streams.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_geared.py registered in $SECONDS seconds."
sleep 5
SECONDS=0
gears-cli --host 10.144.17.211 --port 6379 symspell_sentences_streamed.py --requirements requirements_gears_symspell.txt
echo "symspell_sentences_streamed.py registered in $SECONDS seconds."
sleep 5 
SECONDS=0
gears-cli --host 10.144.17.211 --port 6379 tokenizer_bert_stream.py --requirements requirements_tokenizer.txt 
echo "tokenizer_bert_stream.py registered in $SECONDS seconds."
sleep 5
SECONDS=0
python RedisIntakeRedisClusterSample.py 
echo "RedisIntakeRedisClusterSample.py finished in $SECONDS seconds."
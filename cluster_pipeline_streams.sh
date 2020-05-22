gears-cli --host 10.144.17.211 --port 30001 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt

SECONDS=0
gears-cli --host 10.144.17.211 --port 30001 spacy_sentences_streams.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_geared.py registered in $SECONDS seconds."

SECONDS=0
gears-cli --host 10.144.17.211 --port 30001 symspell_sentences_streamed.py --requirements requirements_gears_symspell.txt
echo "symspell_sentences_geared.py registered in $SECONDS seconds."

SECONDS=0
python RedisIntakeRedisClusterSample.py 
echo "RedisIntakeLocal.py finished in $SECONDS seconds."
gears-cli --host 10.144.83.129 --port 6379 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt

SECONDS=0
gears-cli --host 10.144.83.129 --port 6379 spacy_sentences_geared.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_geared.py registered in $SECONDS seconds."
SECONDS=0
gears-cli --host 10.144.83.129 --port 6379 symspell_sentences_geared.py --requirements requirements_gears_symspell.txt
echo "symspell_sentences_geared.py registered in $SECONDS seconds."

SECONDS=0
python RedisIntakeRedisCluster.py 
echo "RedisIntakeLocal.py finished in $SECONDS seconds."
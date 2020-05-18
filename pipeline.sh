
SECONDS=0
python RedisIntakeLocal.py 
echo "RedisIntakeLocal.py finished in $SECONDS seconds."
SECONDS=0
gears-cli --host 127.0.0.1 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt
echo "lang_detect_gears_paragraphs.py finished in $SECONDS seconds."
SECONDS=0
gears-cli --host 127.0.0.1 spacy_sentences_geared.py --requirements requirements_gears_spacy.txt
echo "spacy_sentences_geared.py finished in $SECONDS seconds."
SECONDS=0
gears-cli --host 127.0.0.1 --port 6379 tokenizer_bert_geared.py --requirements requirements_tokenizer.txt
echo "tokenizer_geared.py finished in $SECONDS seconds."
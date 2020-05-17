# python RedisIntakeLocal.py 
gears-cli --host 10.144.133.112 --port 6379 lang_detect_gears_paragraphs.py --requirements requirements_gears.txt
gears-cli --host 10.144.133.112 --port 6379 spacy_sentences_geared.py --requirements requirements_gears_spacy.txt
gears-cli --host 10.144.133.112 --port 6379 tokenizer.py --requirements requirements_tokenizer.txt

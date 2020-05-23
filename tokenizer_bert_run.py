"""
This is easy to debug version of tokeniser
"""
tokenizer = None 


def loadTokeniser():
    global tokenizer
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    return tokenizer

def tokenise_sentence(record):
    global tokenizer
    if not tokenizer:
        tokenizer=loadTokeniser()
    sentence_key=record['key']
    sentence_orig=record['value']
    # sentence_key=record['value']['sentence_key']
    # sentence_orig=record['value']['content']
    try:
        from spacy.lang.en.stop_words import STOP_WORDS
    except:
        log(f"Stop words are not available ")
    shard_id=hashtag()
    log(f"Tokeniser received {sentence_key} and my {shard_id}")
    tokens = set(tokenizer.tokenize(sentence_orig))
    if STOP_WORDS:
        tokens.difference_update(STOP_WORDS)
    key = "tokenized:bert:%s:{%s}" % (sentence_key,shard_id)
    execute('SADD', key, tokens)
    execute('SADD','processed_docs_stage3_tokenized{%s}' % shard_id, key)


bg = GearsBuilder()
bg.foreach(tokenise_sentence)
bg.count()
bg.run('sentences:*')

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
    shard_id=hashtag()
    log(f"Tokeniser received {sentence_key} and my {shard_id}")
    tokens = tokenizer.tokenize(sentence_orig)
    key = "tokenized:bert:%s:{%s}" % (sentence_key,shard_id)
    for token in tokens:
        execute('lpush', key, token)
        execute('SADD','processed_docs_stage3_tokenized', sentence_key)


bg = GearsBuilder()
bg.foreach(tokenise_sentence)
bg.count()
bg.run('sentences:*')

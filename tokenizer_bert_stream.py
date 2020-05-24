"""
This is a tokenizer using pre-train Bio_Clinical BERT model.
TODO: evaluate if using this as part of spacy-tokeniser on previous step.
Challenge: memory consumption - scispacy small model takes 9 GB in RAM
hence was the reason to split tokeniser into separate one. 
Additional steps can be added by adding a stream instead of set.
TODO: increase batch size: Transformers optimised for batch processing
 increase batch size 
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
    sentence_key=record['value']['sentence_key']
    sentence_orig=record['value']['content']
    shard_id=hashtag()
    key = "tokenized:bert:%s:{%s}" % (sentence_key,shard_id)
    # log(f"Tokeniser received {sentence_key} and my {shard_id}")
    tokens = tokenizer.tokenize(sentence_orig)
    for token in tokens:
        execute('lpush', key, token)
    execute('SADD','processed_docs_stage3_tokenized{%s}' % shard_id, key)


bg = GearsBuilder('StreamReader')
bg.foreach(tokenise_sentence)
bg.count()
bg.register('sentence_to_tokenise_*', batch=1, mode="async_local", onRegistered=loadTokeniser, onFailedPolicy='continue', trimStream=True)


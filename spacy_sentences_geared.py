import en_core_web_sm
nlp = en_core_web_sm.load(disable=['ner','tagger'])
nlp.max_length=1200000

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    key_prefix="en:paragraphs:"
    #make sure we only process english article
    paragraphs =x['value']
    doc=nlp(paragraphs)
    idx=1
    article_id=remove_prefix(x['key'],key_prefix)
    for each_sent in doc.sents:
        sentence_key=f"sentences:{article_id}:{idx}"
        execute('SET', sentence_key, each_sent)
        idx+=1
        execute('SADD','processed_docs_stage2_sentence', article_id)
        log("Successfully processed paragraphs "+str(article_id),level='notice')
    else:
        execute('SADD','screw_ups', x['key'])
    

gb = GB()
gb.repartition(lambda x: int(len(x['value'])))
gb.foreach(parse_paragraphs)
gb.count()
gb.register('en:paragraphs:*',keyTypes=['string'])
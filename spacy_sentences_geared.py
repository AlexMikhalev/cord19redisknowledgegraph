nlp = None

def OnRegistered():
    global nlp
    import en_core_web_sm
    nlp = en_core_web_sm.load(disable=['ner','tagger'])

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    global nlp
    key_prefix="en:"
    paragraphs =x['value']
    article_id = remove_prefix(x['key'],key_prefix)
    doc=nlp(paragraphs)
    idx=1
    for each_sent in doc.sents:
        sentence_key="sentences:%s:%s:{%s}" % (article_id, idx,hashtag())
        execute('SET', sentence_key, each_sent)
        idx+=1
        execute('SADD','processed_docs_stage2_sentence{%s}' % hashtag(), article_id)
        log("Successfully processed paragraphs "+str(article_id),level='notice')
    

GB().foreach(parse_paragraphs).count().register('en:*', keyTypes=['string'], onRegistered=OnRegistered, mode="async_local")
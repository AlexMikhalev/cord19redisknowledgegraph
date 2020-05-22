# FIXME: don't use it, streams are better solution
nlp = None

def load_nlp_object():
    import en_core_web_sm
    log("Importing NLP")
    nlp = en_core_web_sm.load(disable=['ner','tagger'])
    nlp.max_length=1200000
    return nlp


def OnRegistered():
    global nlp
    nlp=load_nlp_object()
    return nlp


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    global nlp
    key_prefix="en:"
    paragraphs =x['value']
    article_id = remove_prefix(x['key'],key_prefix)
    if not nlp:
        nlp=load_nlp_object()
    doc=nlp(paragraphs)
    idx=1
    for each_sent in doc.sents:
        sentence_key="sentences:%s:%s:{%s}" % (article_id, idx, hashtag())
        execute('SET', sentence_key, each_sent)
        idx+=1
        execute('XADD', 'processed_docs_stage2_sentence{%s}' % hashtag(), '*', 'key', f"{sentence_key}")
        log(f"Successfully processed paragraphs {sentence_key}",level='notice')
    
GB().foreach(parse_paragraphs).count().run('en:*', keyTypes=['string'], onRegistered=OnRegistered, mode="async_local")
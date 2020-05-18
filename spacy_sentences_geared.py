import spacy 
nlp=spacy.load('en_core_web_md', disable=['ner','tagger'])

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    key_prefix="paragraphs:"
    #make sure we only process english article
    lang=execute('GET', 'lang_article:' + x['key'])
    if lang=='en':
        paragraphs =x['value']
        doc=nlp(paragraphs)
        idx=1
        article_id=remove_prefix(x['key'],key_prefix)
        for each_sent in doc.sents:
            sentence_key=f"sentences:{article_id}:{idx}"
            execute('SET', sentence_key, each_sent)
            idx+=1
        execute('SADD','processed_docs_stage2_sentence', article_id)
    else:
        execute('SADD','screw_ups', x['key'])
    

gb = GB()
gb.foreach(parse_paragraphs)
gb.count()
gb.run('paragraphs:*')
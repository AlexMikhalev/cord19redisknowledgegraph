import spacy 
nlp=spacy.load('en_core_web_md', disable=['ner','tagger'])

def parse_paragraphs(x):
    #detect language of the article
    lang=execute('GET', 'lang_article:' + x['key'])
    if lang=='en':
        paragraphs =x['value']
        doc=nlp(paragraphs)
        idx=1
        article_id=x['key']
        for each_sent in doc.sents:
            sentence_key=f"tokens:{article_id}:{idx}"
            execute('SET', sentence_key, each_sent)
            idx+=1
        execute('SADD','processed_docs_stage2_sentence', article_id)
    else:
        execute('SADD','articles_to_delete', x['key'])
    

gb = GB()
gb.foreach(parse_paragraphs)
gb.run('paragraphs:*')
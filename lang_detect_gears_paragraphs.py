from langdetect import detect   

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def detect_language(record):
    #detect language of the article
    try:
        lang=detect(record['value'][:1000])
    except:
        lang="empty"
    if lang=='en':
        article_id = remove_prefix(record['key'],'paragraphs:') 
        paragraph_key="en:{%s}:" % article_id
        execute('SET', paragraph_key, record['value'])
        log(f"Success lang {paragraph_key}",level='notice')
        log('Hashtag {%s}' % hashtag())
        execute('SADD','successfull_lang{%s}' % hashtag(), paragraph_key)
    else:
        log("Failed to detect language: "+str(record['key']),level='notice')
        execute('SADD','articles_to_delete', record['key'])

gb = GB()
gb.foreach(detect_language)
gb.register('paragraphs:*',keyTypes=['string'], mode="async_local")
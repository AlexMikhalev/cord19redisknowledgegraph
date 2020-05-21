from langdetect import detect   

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def detect_language(record):
    #detect language of the article
    value=record['value']
    try:
        lang=detect(value[:1000])
    except:
        lang="empty"
    if lang=='en':
        article_id = remove_prefix(record['key'],'paragraphs:') 
        paragraph_key="en:%s:{%s}" % (article_id, hashtag())
        log(f"Success lang {paragraph_key}",level='notice')
        execute('SET', paragraph_key, value)
        execute('SADD','successfull_lang{%s}' % hashtag(), paragraph_key)
    else:
        log("Failed to detect language: "+str(record['key']),level='notice')
        execute('SADD','articles_to_delete', record['key'])

gb = GB()
gb.foreach(detect_language)
gb.register('paragraphs:*',keyTypes=['string'], mode="sync")
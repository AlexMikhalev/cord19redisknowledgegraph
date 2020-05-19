from langdetect import detect   
from redisgears import log

def detect_language(record):
    #detect language of the article
    try:
        lang=detect(record['value'][:1000])
    except:
        lang="empty"
    execute('SET', 'lang_article:' + record['key'], lang)
    log("Success "+str(record['key']),level='notice')
    if lang!='en':
        log(str(record['key']),level='notice')
        execute('SADD','articles_to_delete', record['key'])

gb = GB()
gb.foreach(detect_language)
gb.count()
gb.register('paragraphs:*',keyTypes=['string'])
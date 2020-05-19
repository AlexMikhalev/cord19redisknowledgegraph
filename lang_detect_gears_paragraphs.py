from langdetect import detect   
from redisgears import log

def detect_language(record):
    #detect language of the article
    try:
        lang=detect(record['value'][:1000])
    except:
        lang="empty"
    if lang=='en':
        execute('SET', 'en:' + record['key'], record['value'])
        log("Success "+str(record['key']),level='notice')
    else:
        log("Failed to detect language: "+str(record['key']),level='notice')
        execute('SADD','articles_to_delete', record['key'])

gb = GB()
gb.foreach(detect_language)
gb.count()
gb.register('paragraphs:*',keyTypes=['string'])
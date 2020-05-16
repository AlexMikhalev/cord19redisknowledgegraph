from langdetect import detect   

def detect_language(x):
    #detect language of the article
    try:
        lang=detect(x['value'])
    except:
        lang="empty"
    execute('SET', 'lang_article:' + x['key'], lang)
    if lang!='en':
        execute('SADD','titles_to_delete', x['key'])

gb = GB()
gb.foreach(detect_language)
gb.run('title:*')
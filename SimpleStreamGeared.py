def log_stream(x):
    log("My cluster %s" % hashtag())
    log("Test log Steam Key %s" % x['key'])
    log("Test log article id %s " % x['value']['article_id'])
    log("Test log content %s " % x['value']['content'][:100])

bg = GearsBuilder('StreamReader')
bg.foreach(log_stream)
bg.register('sentences_spellcheck*', batch=1, mode="async_local", onFailedPolicy='continue', trimStream=True)

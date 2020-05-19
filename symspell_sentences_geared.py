from redisgears import log


import pkg_resources
from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
bigram_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def symspell_sentences(record):
    key_prefix='sentences:'
    sentence_orig=execute('GET', record['key'])
    # max edit distance per lookup (per single word, not per whole input string)
    suggestions = sym_spell.lookup_compound(sentence_orig, max_edit_distance=2,
                                        transfer_casing=True, ignore_non_words=True)
    sentence_key="symspelled:" + remove_prefix(record['key'],key_prefix)
    execute('SET', sentence_key, suggestions[0].term)
    log("Successfully spellchecked sentence "+str(sentence_key),level='notice')
    
gb = GB()
gb.foreach(symspell_sentences)
gb.count()
gb.register('sentences:*',keyTypes=['string'])
import torch
from transformers import AutoTokenizer, AutoModel

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

def parse_sentence(record):
	tokens = tokenizer.tokenize(record['value'])
	key_prefix='sentences:'
	sentence_key=remove_prefix(record['key'],key_prefix)
	for token in tokens:
		key = f"tokenized:bert:{sentence_key}"
		execute('lpush', key, token)
	execute('SADD','processed_docs_stage3_tokenized', sentence_key)

gb = GB()
gb.foreach(parse_sentence)
gb.count()
gb.run('sentences:*')

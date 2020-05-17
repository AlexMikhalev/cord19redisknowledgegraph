import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

def parse_para(sentence_meta):
	tokens = tokenizer.tokenize(sentence_meta['value'])
	push_list({
		'sentence': sentence_meta['value'],
		'sentence_id' : sentence_meta['key'].split(':')[1],
		'tokenized': tokens
	})

def push_list(meta):
	tokens = list(meta['tokenized'])
	key = f"token:{meta['sentence_id']}:{len(tokens)}"
	for token in meta['tokenized']:
		execute('lpush', key, token)

gb = GB()
gb.foreach(parse_para)
gb.run('paragraphs:*')

print(gb)
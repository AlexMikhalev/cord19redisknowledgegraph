import torch
from transformers import AutoTokenizer, AutoModel
from gearsclient import GearsRemoteBuilder as GearsBuilder
import redis
from gearsclient import execute
# conn = redis.Redis(host='10.144.211.47', port=6379)
conn = redis.Redis(host='127.0.0.1', port=6379)

tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")

def parse_para(sentences_ids):
	sentences = []
	for sentence_id in sentences_ids:
		sentences.append({
			'sentence': execute('get', sentence_id),
			'sentence_id' : sentence_id.split(':')[1]
		})
	return sentences

def push_list(meta):
	tokens = list(meta['tokenized'])
	key = f"token:{meta['sentence_id']}:{len(tokens)}"
	for token in meta['tokenized']:
		execute('lpush', key, token)

res = GearsBuilder('KeysOnlyReader', r=conn).\
	  map(lambda x:execute('keys', 'paragraphs:*')).\
	  flatmap(lambda x: parse_para(x)).\
	  flatmap(lambda x:  {'tokenized' : tokenizer.tokenize(x['sentence']), 'sentence_id':x['sentence_id']}).\
	  map(lambda x: push_list(x)).\
	  run()

print(res)
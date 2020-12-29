In [30]: hist                                                                                                            
from qasearch.qa_bert import *
    global tokenizer, model 

    if not tokenizer:
        tokenizer=loadTokeniser()

    if not model:
        model=loadModel()
model
tokenizer
from sample_data.sample_data import *
paragraph
paragraphs
sentence
sentence2
tokenizer.encode(sentence)
tokenizer.encode_plus(sentence)
tokenizer.encode_plus(sentence,add_special_tokens=True, return_tensors="pt")
tokenizer.encode_plus(sentence,add_special_tokens=True)
input_sentence=tokenizer.encode_plus(sentence,add_special_tokens=True)
input_sentence
inputs_ids=tokenizer.encode(sentence)
input_sentence['input_ids']
input_sentence['input_ids'].tolist()
input_sentence['input_ids']
inputs_sentence_pt = tokenizer.encode_plus(sentence, add_special_tokens=True, return_tensors="pt")
input_sentence_pt['input_ids']
inputs_sentence_pt['input_ids']
type(inputs_sentence_pt['input_ids'])
inputs_sentence_pt['input_ids'].toList()
inputs_sentence_pt['input_ids'].tolist()
inputs_sentence_pt['input_ids'].tolist()[0]
inputs_sentence_pt['input_ids'].tolist()[0]
inputs_sentence_pt['input_ids'].tolist()[0]
his
hist

In [31]: input_sentence['input_ids']                                                                                     
Out[31]: 
[101,
 1996,
 4906,
 2005,
 1996,
 2878,
 1997,
 3304,
 7137,
 1996,
 2206,
 16381,
 1045,
 29657,
 1998,
 3141,
 12450,
 1024,
 102]

In [32]: inputs_sentence_pt['input_ids'].tolist()[0]==input_sentence['input_ids']                                        
Out[32]: True

In [33]: bool(inputs_sentence_pt['input_ids'].tolist()[0]==input_sentence['input_ids'])                                  
Out[33]: True

In [34]: tokenizer.sep_token_id                                                                                          
Out[34]: 102

In [35]: tokenizer.special_tokens_map                                                                                    
Out[35]: 
{'unk_token': '[UNK]',
 'sep_token': '[SEP]',
 'pad_token': '[PAD]',
 'cls_token': '[CLS]',
 'mask_token': '[MASK]'}

In [36]: tokenizer.unk_token_id                                                                                          
Out[36]: 100

In [37]: tokenizer.pad_token_id                                                                                          
Out[37]: 0

In [38]: tokenizer.cls_token_id                                                                                          
Out[38]: 101


from qasearch.qa_bert import *
    global tokenizer, model 

    if not tokenizer:
        tokenizer=loadTokeniser()

    if not model:
        model=loadModel()
model
tokenizer
from sample_data.sample_data import *
paragraph
paragraphs
sentence
sentence2
tokenizer.encode(sentence)
tokenizer.encode_plus(sentence)
tokenizer.encode_plus(sentence,add_special_tokens=True, return_tensors="pt")
tokenizer.encode_plus(sentence,add_special_tokens=True)
input_sentence=tokenizer.encode_plus(sentence,add_special_tokens=True)
input_sentence
inputs_ids=tokenizer.encode(sentence)
input_sentence['input_ids']
input_sentence['input_ids'].tolist()
input_sentence['input_ids']
inputs_sentence_pt = tokenizer.encode_plus(sentence, add_special_tokens=True, return_tensors="pt")
input_sentence_pt['input_ids']
inputs_sentence_pt['input_ids']
type(inputs_sentence_pt['input_ids'])
inputs_sentence_pt['input_ids'].toList()
inputs_sentence_pt['input_ids'].tolist()
inputs_sentence_pt['input_ids'].tolist()[0]
inputs_sentence_pt['input_ids'].tolist()[0]
inputs_sentence_pt['input_ids'].tolist()[0]
his
hist
input_sentence['input_ids']
inputs_sentence_pt['input_ids'].tolist()[0]==input_sentence['input_ids']
bool(inputs_sentence_pt['input_ids'].tolist()[0]==input_sentence['input_ids'])
tokenizer.sep_token_id
tokenizer.special_tokens_map
tokenizer.unk_token_id
tokenizer.pad_token_id
tokenizer.cls_token_id
bool(inputs_sentence_pt['input_ids'].tolist()[0]==input_sentence['input_ids'])
question="Effectiveness of inter/inner travel restriction"
question
tokenizer.encode(question)
tokenizer.encode(question)
inputs_question=tokenizer.encode(question)
inputs_question
inputs_full = tokenizer.encode(question, sentence)
inputs_full
inputs_question
inputs_sentence_ids=tokenizer.encode(sentence)
inputs_sentence_ids
inputs_sentence_ids.remove(tokenizer.sep_token_id)
inputs_sentence_ids
inputs_question
inputs_all_handcrafted=inputs_question+inputs_sentence_ids
inputs_all_handcrafted
inputs_question

TODO:pre tokenise using encode 
remove last element if it's id is 'SEP'


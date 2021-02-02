from qasearch.qa_bert import * 
from common.utils import FuncTimer

"""
profiling 
pip install line_profiler

torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

QA_MODEL = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_TOKENIZER = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_MODEL.to(torch_device)
QA_MODEL.eval()
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
"""

def qatest(question, content_text):
    global tokenizer, model 

    if not tokenizer:
        tokenizer=loadTokeniser()

    if not model:
        model=loadModel()

    inputs = tokenizer.encode_plus(question, content_text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(
        answer_start_scores
    )  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    return answer


if __name__ == "__main__":
    from sample_data.sample_data import sentence
    questions = [
        "Effectiveness of case isolation/isolation of exposed individuals (i.e. quarantine)",
        "Effectiveness of community contact reduction",
        "Effectiveness of inter/inner travel restriction",
        "Effectiveness of school distancing",
        "Effectiveness of workplace distancing",
        "Effectiveness of a multifactorial strategy prevent secondary transmission",
        "Seasonality of transmission",
        "How does temperature and humidity affect the transmission of 2019-nCoV?",
        "Significant changes in transmissibility in changing seasons?",
        "Effectiveness of personal protective equipment (PPE)"
    ]
    print("Text : ",sentence)
    for each_question in questions:
        with FuncTimer() :
            answer=qa(each_question,sentence)
        print(f"Question: {each_question}")
        print(f"Answer: {answer}")
        
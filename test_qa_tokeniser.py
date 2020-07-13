from qasearch.qa_bert import * 


"""
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

QA_MODEL = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_TOKENIZER = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
QA_MODEL.to(torch_device)
QA_MODEL.eval()
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
"""

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
        answer=qa(each_question,sentence)
        print(f"Question: {each_question}")
        print(f"Answer: {answer}")

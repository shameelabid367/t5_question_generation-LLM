from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from . import initializer

def genQues(input_):
    print('input is',input_)
    tokenizer = T5Tokenizer.from_pretrained('keyword_question_generation_model_v1')
    model = T5ForConditionalGeneration.from_pretrained('keyword_question_generation_model_v1')

    # Define the input keyword
    inputKeyword = input_

    # Generate the question based on the input keyword
    inputSequence = f'generate question: {inputKeyword}'
    inputIds = tokenizer.encode(inputSequence, return_tensors='pt')

    # Generate the question using the model
    outputIds = model.generate(inputIds)
    generatedQuestion = tokenizer.decode(outputIds[0], skip_special_tokens=True)
    
    return generatedQuestion



from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from . import initializer

init = initializer.init

class genT5():
    def genT5_():
        try:
            global keyCollection

            trainKeys = init.keyCollection.find_one({"type": 'train'})

            if trainKeys is None or 'train' not in trainKeys:
                raise ValueError("Invalid training data or key structure.")

            keywordQuestions = trainKeys['train']

            # Load the existing tokenizer and T5 model
            tokenizer = T5Tokenizer.from_pretrained('t5-base')
            model = T5ForConditionalGeneration.from_pretrained('t5-base')

            # Set the batch size
            batchSize = 32

            # Prepare the new training data
            newKeywords = [{"module": item["module"].lower(), "role": item["role"].lower(), "key": item["key"].lower()} for item in keywordQuestions]
            newQuestions = [item['ques'] for item in keywordQuestions]

            # Prepare the data for fine-tuning
            inputSequences = [f'generate question: {keyword}' for keyword in newKeywords]
            inputIds = tokenizer.batch_encode_plus(inputSequences, padding=True, return_tensors='pt').input_ids

            # Tokenize the target questions
            targetIds = tokenizer.batch_encode_plus(newQuestions, padding=True, return_tensors='pt').input_ids

            # Create DataLoaders
            trainDataloader = torch.utils.data.DataLoader(list(zip(inputIds, targetIds)), batch_size=batchSize)

            # Define the training loop
            optimizer = torch.optim.Adam(params=model.parameters(), lr=1e-4)
            numEpochs = 70

            for epoch in range(numEpochs):
                for batch in trainDataloader:
                    try:
                        inputIds, targetIds = batch
                        optimizer.zero_grad()
                        outputs = model(input_ids=inputIds, labels=targetIds)
                        loss = outputs.loss
                        loss.backward()
                        optimizer.step()
                    except Exception as batch_exception:
                        print(f"Error during batch processing: {batch_exception}")

                if (epoch + 1) % 10 == 0:
                    print(f'Epoch [{epoch + 1}/{numEpochs}], Loss: {loss.item():.4f}')

            # Save the retrained model
            model.save_pretrained('keyword_question_generation_model_v1')
            tokenizer.save_pretrained('keyword_question_generation_model_v1')

            return 'Process Completed'

        except Exception as e:
            print(f'Error: {e}')
            return 'Something Wrong Happened'
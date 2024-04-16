# T5 Model Question Generation

## Description
This project uses the T5 text-to-text transformer model to generate questions based on a given module, role, and key. For example, if the module is "Recruitment", the role is "Essential Service", and the key is "name", the model will generate the question "What is your name?". Then we will store the questions to a MongoDB Sever along with its module, role and key.

## Pre-requisite
You should have a MongoDB document with training keys inside **keys** collection
```
{
  "_id": {
    "$oid": "6563183ce8571df19e0e95d3"
  },
  "type": "train",
  "train": [
    {
      "module": "recruitment",
      "role": "company",
      "key": "name",
      "ques": "What is your company name?"
    },
    {
      "module": "recruitment",
      "role": "company",
      "key": "location",
      "ques": "Where is your company located?"
    },
    {
      "module": "recruitment",
      "role": "company",
      "key": "website",
      "ques": "What is the name of your website?"
    },
    {
      "module": "recruitment",
      "role": "job_openings",
      "key": "department",
      "ques": "What is your department?"
    },
    {
      "module": "recruitment",
      "role": "job_openings",
      "key": "position",
      "ques": "What is your position?"
    },
    {
      "module": "recruitment",
      "role": "job_openings",
      "key": "experience",
      "ques": "How much is your experience?"
    },
    {
      "module": "recruitment",
      "role": "job_openings",
      "key": "jobtype",
      "ques": "What is your job type?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "name",
      "ques": "What is your name?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "age",
      "ques": "How old are you?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "dob",
      "ques": "What is your Date of birth?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "email",
      "ques": "What is your email?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "phone",
      "ques": "What is your phone number?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "job_title",
      "ques": "What is your job?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "address",
      "ques": "What is your address?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "interests",
      "ques": "What is your interests?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "hobby",
      "ques": "What is your hobbies?"
    },
    {
      "module": "recruitment",
      "role": "personal",
      "key": "freetime",
      "ques": "How do you spend your free time?"
    },
    {
      "module": "recruitment",
      "role": "softskills",
      "key": "softskills",
      "ques": "What are your softskills?"
    },
    {
      "module": "recruitment",
      "role": "techskills",
      "key": "techskills",
      "ques": "What are your techskills?"
    }
  ]
}
```


## Steps:
1. Connect MongoDB
2. T5 Model Creation
3. Checking Missing Value
4. Asking To User Each Question One by One

# 1. Connect MongoDB
```
client = MongoClient(f"mongodb+srv://<username>:<password>@cluster0.i4eqmas.mongodb.net/")
databaseName = 'MyMobileApp'
collectionName = 'users'
db = client[databaseName]
collection = db[collectionName]
keyCollection = db['keys']
```
**Note:** Replace \<username\> and \<password\> with your own credentials.

# 2. T5 Model Creation

### 1. Install the required dependencies:
```
pip install torch transformers sentencepiece
```

### 2. Load the training JSON file
```
mongoTrainKey = keyCollection.find_one({"type": 'train'})['train']
```

### 3. Import neccessary libraries
```
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
```

### 4. Fine-tune and save the model
```
# Load the existing tokenizer and T5 model
tokenizer = T5Tokenizer.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained('t5-base')

# Set the batch size
batchSize = 32

# Prepare the new training data
newKeywords = [{"module": item["module"].lower(), "role": item["role"].lower(), "key": item["key"].lower()} for item in mongoTrainKey]
newQuestions = [item['ques'] for item in mongoTrainKey]

# Prepare the data for fine-tuning
inputSequences = [f'generate question: {keyword}' for keyword in newKeywords]
inputIds = tokenizer.batch_encode_plus(inputSequences, padding=True, return_tensors='pt').input_ids

# Tokenize the target questions
targetIds = tokenizer.batch_encode_plus(newQuestions, padding=True, return_tensors='pt').input_ids

# Create DataLoaders
trainDataloader = torch.utils.data.DataLoader(list(zip(inputIds, targetIds)), batch_size=batchSize)

# Define the training loop
optimizer = torch.optim.Adam(params=model.parameters(), lr=1e-4)
numEpochs = 100

for epoch in range(numEpochs):
    for batch in trainDataloader:
        inputIds, targetIds = batch
        optimizer.zero_grad()
        outputs = model(input_ids=inputIds, labels=targetIds)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{numEpochs}], Loss: {loss.item():.4f}')

# Save the retrained model
model.save_pretrained('keyword_question_generation_model_v1')
tokenizer.save_pretrained('keyword_question_generation_model_v1')
```

# 3. Checking Missing Value

## 1. Iterate the entire **user** document to check missing values
```
allDocument =initializer.init.collection.find()

if allDocument:
    for i in allDocument:
        try:
            checkempty.checkEmpty(i['context'], i['IMEI'])
        except Exception as inner_exception:
            print(f"Error processing document with IMEI {i['IMEI']}: {inner_exception}")
            return f"Error processing document with IMEI {i['IMEI']}: {inner_exception}"
    print('Process Completed')
    return 'Process Completed'
else:
    # If IMEI not found, return an error response
    return 'User not found'
```
Above code will iterate the entire MongoDB **user** document and check any missing values exists. Missing values will be stored on MongoDB along with generated Questions.

# 4. Asking To User Each Question One by One

## 1. After user gave the answer we will fill the key with user input
```
ans = request.args.get('input_')
query = {"IMEI": initializer.init.IMEI}
doc = initializer.init.collection.find_one(query)

if doc is None:
    raise ValueError("Document not found for the given IMEI.")

role = doc['ques'][0]['role'].lower()
key = doc['ques'][0]['key'].lower()
type = doc['ques'][0]['type']
print('type is', type)

if type == 'list':
    splitAns = ans.split(",")
    doc['context'][0][role] = splitAns
else:
    doc['context'][0][role][key] = ans

initializer.init.collection.update_one({'IMEI': initializer.init.IMEI}, {'$set': doc})
initializer.init.collection.update_one({'IMEI':initializer.init.IMEI}, {'$pop': {'ques': -1}})
```
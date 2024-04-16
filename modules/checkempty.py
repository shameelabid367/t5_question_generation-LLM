from . import initializer
from . import gen_ques

def generateAndAppendQuestion(category, key, data_type):
        ques = gen_ques.genQues({"module":initializer.init.module.lower(), "role": category.lower(), 'key': key.lower()})
        initializer.init.allQues.append({"module":initializer.init.module.lower(), "role": category.lower(), "key": key.lower(), "ques": ques, 'type': data_type})

def updateCollection(IMEI):
    return initializer.init.collection.update_one({"IMEI": IMEI}, {'$set': {'ques': initializer.init.allQues}})

def checkEmpty(schema,IMEI):
    initializer.init.allQues = []
    
    def processDictData(category, data):
        for key, value in data.items():
            if not value:
                generateAndAppendQuestion(category, key, 'dict')

    def processListData(category, data):
        if not data:
            generateAndAppendQuestion(category, category, 'list')

    
    for index, userData in enumerate(schema, start=1):
        for category, data in userData.items():
            if isinstance(data, dict):
                processDictData(category, data)
            elif isinstance(data, list):
                processListData(category, data)
            else:
                raise TypeError('Data type is neither dict nor list')

    if initializer.init.allQues:
        result = updateCollection(IMEI)
    else:
        print('Nothing to update')
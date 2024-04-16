from . import checkempty
from . import initializer

def upload():
    try:
        global mongoTrainKey
        mongoTrainKey = initializer.init.keyCollection.find_one({"type": 'train'})['train']

        # Query the MongoDB collection based on userId
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

    except KeyError as ke:
        print(f'KeyError: {ke}')
        return f'KeyError on upload.py: {ke}'
    except ValueError as ve:
        print(f'ValueError: {ve}')
        return f'ValueError on upload.py: {ve}'
    except Exception as e:
        print(f'Error: {e}')
        return f'Error on upload.py: {e}'

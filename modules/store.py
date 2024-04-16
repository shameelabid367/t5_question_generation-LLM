from . import initializer
from flask import Flask, render_template, request

def store():
    try:
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
        return render_template('redirect.html')

    except KeyError as ke:
        print(f'KeyError: {ke}')
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except Exception as e:
        print(f'Error: {e}')
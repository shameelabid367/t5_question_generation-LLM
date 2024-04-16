from . import initializer
from flask import Flask, render_template, request


def nextQues():
    query = {"IMEI":initializer.init.IMEI}
    doc =initializer.init.collection.find_one(query)

    if not doc:
        return "User not Found :("
    
    if not initializer.init.collection.find_one({'ques': {'$exists': True}}):
        return 'No Generated Questions Available For This User'
    
    if len(doc['ques']) >= 1:
        # ques is not empty
        ques = doc['ques'][0]['ques']
        return render_template('questions.html', ques=ques)
    else:
        return render_template('no_ques.html')
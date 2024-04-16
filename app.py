from flask import Flask, render_template
from modules import upload,gen_t5,store,nextques

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_():
    return upload.upload()

@app.route('/store')
def store_():
    return store.store()

@app.route('/next_ques')
def nextQues():
   return nextques.nextQues()

@app.route('/gen_t5')
def genT5():
    return gen_t5.genT5.genT5_()

if __name__ == '__main__':
    app.run(debug=True)
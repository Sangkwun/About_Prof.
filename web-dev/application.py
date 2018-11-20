from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.hackerton

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    query = request.args.get('query')
    return render_template('result.html', query=query)

@app.route('/professor/<author_id>')
def professor(author_id):
    doc = db.professors.find_one({'Author ID':author_id})
    doc.pop('_id')
    return jsonify(doc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

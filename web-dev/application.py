from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient

import numpy as np
import json

app = Flask(__name__)

client = MongoClient()
db = client.hackerton

PROFESSOR_NUMBER = 258
WORD_NUMBER = 1000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    query = request.args.get('query')
    type = request.args.get('type')


    return render_template('result.html', query=query, type=type)

@app.route('/professor')
def professor():
    name = request.args.get('name')
    doc = db.finaldb.find_one({'Name':name})
    doc.pop('_id')
    return jsonify(doc)

@app.route('/data')
def get_data():
    query = request.args.get('query')
    type = request.args.get('type')
    res_mat = np.random.rand(PROFESSOR_NUMBER+WORD_NUMBER,PROFESSOR_NUMBER+WORD_NUMBER)

    return jsonify(getJSON(query, type, res_mat))


def getJSON(query, query_type, res_mat, threshold=0.92):
    label_map = db.finaldb.distinct("Name") + db.wordname.distinct("wordname")[:1000]
    for i in range(PROFESSOR_NUMBER):
        label_map.append('professor'+str(i))
    for i in range(WORD_NUMBER):
        label_map.append('word'+str(i))
    res_json={
        "nodes": [],
        "links": []
    }
    color_map = {'Graduate School of Technology and Innovation Management(기술경영전문대학원)':'#cd7fb3', 'School of Business Administration(경영학부)':'#cd7fb3', 'School of Electrical and Computer Engineering(전기전자컴퓨터공학부)':'#ea4f6e', 'School of Energy and Chemical Engineering(에너지및화학공학부)':'#52a6b1', 'School of Management Engineering(경영공학부)':'#cd7fb3', 'School of Materials Science and Engineering(신소재공학부)':'#52a6b1', 'School of Mechanical, Aerospace and Nuclear Engineering(기계항공및원자력공학부)':'#52a6b1', 'Graduate School of Creative Design Engineering(디자인-공학 융합전문대학원)':'#f6c431', 'School of Design and Human Engineering(디자인 및 인간공학부)':'#f6c431', 'School of Life Sciences(생명과학부)':'#afcb05', 'School of Natural Science(자연과학부)':'#c4c4c4', 'School of Urban and Environmental Engineering(도시환경공학부)':'#00963f'}
    if query_type == "professor":
        for idx, i in enumerate(res_mat):
            if label_map[idx] == query:
                target = i[:PROFESSOR_NUMBER]
                top_50 = sorted(range(len(target)), key=lambda k: target[k])[-49:]
                if idx not in top_50:
                    top_50.append(idx)
                else:
                    top_50.append(top_50.pop(top_50.index(idx)))

        for jdx, j in enumerate(top_50):
            print(db.finaldb.find_one({"Name":label_map[j]})['department'])
            res_json["nodes"].append({
                "id":label_map[j],
                "chapters": [
                    "1"
                ],
                "name":label_map[j],
                "color":color_map[db.finaldb.find_one({"Name":label_map[j]})['department']]
            })


        for i in top_50:
            target = res_mat[i][:PROFESSOR_NUMBER]
            for jdx, j in enumerate(target):
                if j > threshold and jdx in top_50:
                    res_json["links"].append({
                          "source":label_map[i],
                          "target":label_map[jdx],
                          "similarity":j
                        })

    else:
        for idx, i in enumerate(res_mat):
            if label_map[idx] == query:
                print(i)
                target = i[:PROFESSOR_NUMBER]
                top_50 = sorted(range(len(target)), key=lambda k: target[k])[-49:]
                if idx not in top_50:
                    top_50.append(idx)
                else:
                    top_50.append(top_50.pop(top_50.index(idx)))

        for jdx, j in enumerate(top_50):
            print(db.finaldb.find_one({"Name":label_map[j]})['department'])
            res_json["nodes"].append({
                "id":label_map[j],
                "chapters": [
                    "1"
                ],
                "name":label_map[j],
                "color":color_map[db.finaldb.find_one({"Name":label_map[j]})['department']]
            })


        for i in top_50:
            target = res_mat[i][:PROFESSOR_NUMBER]
            for jdx, j in enumerate(target):
                if j > threshold and jdx in top_50:
                    res_json["links"].append({
                          "source":label_map[i],
                          "target":label_map[jdx],
                          "similarity":j
                        })
    return res_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

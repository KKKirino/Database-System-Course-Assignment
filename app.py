import pyodbc
from flask import Flask, jsonify, request, abort
import json
app = Flask(__name__)

server = 'DESKTOP-BBKEC14\SQLEXPRESS'
database = 'EX'
username = 'sa'
password = '123'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/user/get/<int:id>')
def get(id):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * from author where authorID = %d" %(id))
    result=cursor.fetchone() 
    return {
        "authorID": result[0],
        "authorName": result[1]
    }
@app.route('/user/del/<int:id>')
def dele(id):
    cursor = cnxn.cursor()
    cursor.execute("DELETE from author where authorID = %d" %(id))
    cursor.execute("SELECT * from author")
    result=cursor.fetchall()
    for row in result:
        print(row)
    return "Delect successfully!"

@app.route('/post-sum', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        return {
            "res": data['x'] + data['y']
        }

@app.route('/user/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        cursor = cnxn.cursor()
        name = data['name']
        ID = data['ID']
        cursor.execute("insert into author(authorID, authorName) values(%d, '%s')" % (ID, name))
        cursor.execute("SELECT * from author")
        result=cursor.fetchall()
        for row in result:
            print(row)
        return {
            "ok": "true"
        }

@app.route('/user/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = request.get_json()
        cursor = cnxn.cursor()
        name = data['name']
        ID = data['ID']
        cursor.execute("UPDATE author SET authorID = '%d' WHERE authorName = '%s'" % (ID, name))
        cursor.execute("SELECT * from author")
        result=cursor.fetchall()
        for row in result:
            print(row)
        return {
            "ok": "true"
        }

app.run(host='127.0.0.1', port=1234)



import pyodbc
from flask import Flask, jsonify, request, abort, render_template
import json
app = Flask(__name__, static_folder='./template/static', template_folder='./template')

server = 'DESKTOP-BBKEC14\SQLEXPRESS'
database = 'EX'
username = 'sa'
password = '123'
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

@app.route("/subject")
def home():
    cursor = cnxn.cursor()
    cursor.execute("select subjectName, subjectID from dbo.subject where parentID = 0")
    result=cursor.fetchall()
    cnxn.commit() 
    return jsonify([{ 'name': r[0], 'id': r[1] } for r in result])

@app.route("/subsubject/side-item-name-<int:id>")
def subhome(id):
    cursor = cnxn.cursor()
    cursor.execute("select subjectName, subjectID from dbo.subject where parentID = %d" %(id))
    result=cursor.fetchall()
    cnxn.commit() 
    for row in result:
        print(row)
    return jsonify([{ 'name': r[0], 'id': r[1] } for r in result])

@app.route("/course/sub-sub-item-name-<int:id>")
def course(id):
    cursor = cnxn.cursor()
    cursor.execute("select courseID from dbo.course_subject where subjectID = %d" %(id))
    result1=cursor.fetchall()
    finalres = []
    for r in result1:
        cursor.execute("select courseID, courseName, author, source from dbo.CourseItem where courseID = %d" %(r[0]))
        tempres = cursor.fetchone() 
        finalres.append({'id':tempres[0], 'name':tempres[1], 'author':tempres[2], 'src':tempres[3]})
    cnxn.commit() 
    for row in result1:
        print(row)
    return jsonify(finalres)

@app.route("/subsubsubject/sub-item-name-<int:id>")
def subsubhome(id):
    cursor = cnxn.cursor()
    cursor.execute("select subjectName, subjectID from dbo.subject where parentID = %d" %(id))
    result=cursor.fetchall()
    cnxn.commit() 
    for row in result:
        print(row)
    return jsonify([{ 'name': r[0], 'id': r[1] } for r in result])

@app.route('/user/get/<int:id>')
def get(id):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * from author where authorID = %d" %(id))
    result=cursor.fetchone() 
    cnxn.commit() 
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
    cnxn.commit()
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
        cnxn.commit()
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
        cnxn.commit()
        for row in result:
            print(row)
        return {
            "ok": "true"
        }

app.run(host='127.0.0.1', port=1234, debug=True)



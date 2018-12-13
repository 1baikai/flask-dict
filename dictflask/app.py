from datetime import datetime

from flask import Flask, render_template, request, redirect, json
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost:3306/dict"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SECRET_KEY']='zhaogenvpengyou'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    passwd = db.Column(db.String(16),nullable=True,default=000000)

    def __init__(self,name,passwd):
        self.name=name
        self.passwd=passwd

class Hist(db.Model):
    __tablename__='hist'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    word = db.Column(db.String(32))
    time = db.Column(db.DateTime)

    def __init__(self,name,word,time):
        self.word=word
        self.time=time
        self.name=name



class Words(db.Model):
    __tablename__='words'
    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(32))
    interpret = db.Column(db.Text)



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        # print(name)
        passwd = request.form.get('passwd')
        name1 = Users.query.filter_by(name = name).first()
        if name1:
            if passwd==name1.passwd:
                return render_template('queryword.html',name=name1)
        else:
            return "登录失败"


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        name = request.form.get('name')
        passwd = request.form.get('passwd')
        user = Users.query.filter_by(name=name).first()
        if user:
            return "用户名重复"
        else:
            user = Users(name,passwd)
            db.session.add(user)
            return render_template('login.html')

@app.route('/queryword')
def query_word():
    return render_template('queryword.html')

@app.route('/queryword-server')
def query_word1():

    word = request.args.get('nword')
    name = request.args.get('name')
    time = str(datetime.now())
    # print(type(time))
    # print(word,name,time)
    hist = Hist(name,word,time)
    db.session.add(hist)

    # print(word)
    word = Words.query.filter_by(word=word).first()
    if word is None:
        return "没有该单词"
    else:

        return word.interpret

@app.route('/query-hist')
def query_hist():
    name = request.args.get('name')
    hist = Hist.query.filter(Hist.name==name).limit(10).all()
    list = []

    for i in hist:
        dic={'name':i.name,
             'word':i.word,
             'time':i.time,}

        list.append(dic)


    return json.dumps(list)




if __name__ == '__main__':
    app.run()

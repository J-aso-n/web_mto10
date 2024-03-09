from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from os import path
import pymysql
import time
import json

app = Flask(__name__)

app.secret_key = 'my_secret_key'
def connect_to_db():
    # 连接数据库
    server = 'localhost'  # 服务器名称或IP地址
    database = 'myplayers'  # 数据库名称
    username = 'root'  # 用户名
    password = '12345678'  # 密码
    #print('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cnxn = pymysql.connect(host=server,user=username,password=password,database=database)
    return cnxn

@app.route('/')
def init():
    return redirect('/login')
#**********************登陆注册部分*******************************
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        s = request.form['Submit']
        if s == '注册':
            return redirect('/register')
        cnxn = connect_to_db()
        cursor = cnxn.cursor()
        query = "SELECT * FROM data WHERE username = '{}' AND password = '{}'".format(username, password)
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            session['username'] = user[0]
            return redirect('/login_success')
        else:
            return '登录失败，请检查用户名和密码是否正确！请返回'
    else:
        return render_template('login.html')
@app.route('/login_success')
def login_success():
    if 'username' in session:
        username = session['username']
        cnxn = connect_to_db()
        cursor = cnxn.cursor()

        query_username = "SELECT * FROM data"
        cursor.execute(query_username)
        user = cursor.fetchall()
        user=list(user)

        cnxn.close()
        #user = list(user)

        user.sort(key=lambda x: x[2], reverse=True)

        order = len(user)

        return render_template('合成十.html', username=username, user=user, order=order)
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #render_template('zhuce.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            return '两次输入的密码不一致，请重新输入！'          #yes
        else:
            cnxn = connect_to_db()
            cursor = cnxn.cursor()
            query = "INSERT INTO data (username, password, score) VALUES ('{}', '{}', '{}')".format(username, password2, '0')     #向数据库中插入新数据，也就是注册过程
            cursor.execute(query)
            cnxn.commit()
            return redirect('/register_success')
    else:
        return render_template('zhuce.html')

@app.route('/register_success')
def register_success():
    #render_template('register_success.html')
    #time.sleep(2)
    return render_template('login.html')
#********************************************************************


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        username = session['username']
        score = str(request.values.get("sum"))# 获取结束时分数
        cnxn = connect_to_db()
        cursor = cnxn.cursor()
        # 更新
        query = "UPDATE data SET data.score = '{}' WHERE data.username = '{}'".format(score, username)  # 向数据库中插入新数据，也就是注册过程
        cursor.execute(query)
        cnxn.commit()
        cnxn.close()


        return redirect('/login_success')

    else:
        return render_template('合成十.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8987, debug=True)

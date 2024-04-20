from flask import Flask, render_template, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
import sqlite3 as sql
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '42d375b8b3a640d9ba56f495be6378c8'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert' : 'Token is Missing'})
        try:
            payload = jwt.decode(token, app.config['SECRET KEY'])
        except:
            return jsonify({'Alert!' : 'Invalid Token!'})
    return decorated

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in Currently'


@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'

@app.route('/enternew')
def new_assignment():
    return render_template('assignment.html')

@app.route('/updatenew')
def update_assignment():
    return render_template('update.html')

@app.route('/loginuser')
def login_user():
    return render_template('login.html')

@app.route('/deleterec')
def delete_assignment():
    return render_template('delete.html')

@app.route('/registeruser')
def register_user():
    return render_template('register.html')



@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        try:
            ide = request.form['id']
            nm = request.form['name']
            password = request.form['pass']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (id,username,password) VALUES (?,?,?)",(ide,nm,password))
                con.commit()
                msg = "Record successfully added"
            
        except:
            con.rollback()
            msg = "Error in insertion operation"

        finally:
            return render_template("result.html",msg=msg)
            con.close()

def get_user(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    con.close()
    return user
        
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('name')
    password = request.form.get('pass')
    if username and password==get_user(username):
        session['logged_in'] = True
        token = jwt.encode({
            'user' : request.form['username'],
            'expiration' : str(datetime.utcnow() + timedelta(seconds=120))
        },
        app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('utc-8')})
    else:
        return make_response('Unable to verify',403,{'WWW-Authenticate' : 'Basic realm: Authentication failed'})


   

@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            ide = request.form['id']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['leader']
            date = request.form['ded']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO assignments (id,name,mentor,leader,deadline) VALUES (?,?,?,?,?)",(ide,nm,addr,city,date))
                con.commit()
                msg = "Record successfully added"
            
        except:
            con.rollback()
            msg = "Error in insertion operation"

        finally:
            return render_template("result.html",msg=msg)
            con.close()

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        try:
            ide = request.form['id']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['leader']
            date = request.form['ded']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE assignments SET name=?, mentor=?, leader=?, deadline=? WHERE id=?", (nm, addr, city, date, ide))
                con.commit()
                msg = "Record successfully updated"
            
        except:
            con.rollback()
            msg = "Error in update operation"

        finally:
            con.close()
            return render_template("result.html",msg=msg)
        
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        try:
            ide = request.form['id']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM assignments WHERE id=?", (ide,))
                con.commit()
                msg = "Record successfully deleted"
            
        except:
            con.rollback()
            msg = "Error in deletion operation"

        finally:
            con.close()
            return render_template("result.html",msg=msg)
        
@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from assignments")
    rows = cur.fetchall()
    return render_template("list.html",rows=rows)
if __name__ == '__main__':
    app.run(debug=True)
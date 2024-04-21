from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = '42d375b8b3a640d9ba56f495be6378c8'

@app.route('/')
def home():
    return render_template('home.html')

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

def get_user(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    con.close()
    return user

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
        
@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('id')
    username = request.form.get('name')
    password = request.form.get('pass')

    if not username or not password:
        return render_template('fail.html', message='Username and password are required'), 400

    # In a real application, you would authenticate the user based on the provided username and password.
    # For demonstration purposes, we'll just use a hardcoded user ID here.
    
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        if user and check_password_hash(user[2], password):
            # User exists and password matches, generate JWT token
            token = jwt.encode({'user_id': user[0]}, app.config['SECRET_KEY'], algorithm='HS256')
            return render_template('success.html', token=token.decode('UTF-8'))
        # User does not exist or password does not match
        return render_template('login.html', message='Invalid username or password'), 401

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

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlite3
import random

# DB connection
app = Flask(__name__)
app.config["SESSION_TIMEOUT"] = 360
app.secret_key = 'cs50_final_project'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    db = sqlite3.connect("songs.db").cursor()
    db.execute("SELECT * FROM songs ORDER BY RANDOM() LIMIT 18")
    songs = db.fetchall()
    db.close()
    return render_template("index.html", songs=songs)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = sqlite3.connect("songs.db").cursor()
        username = request.form.get("email")
        password = request.form.get("password")

        if not username:
            return render_template("login.html", error="Please enter a email")
        elif not password:
            return render_template("login.html", error="Please enter a password")

        user = db.execute("SELECT * FROM users WHERE user = ?", (username,)).fetchone()

        if not user or not check_password_hash(user[2], password):
            return render_template("login.html", error="Invalid email and/or password")

        session['user_id'] = user[0]
        session['user_name'] = user[1]

        db.close()
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = sqlite3.connect("songs.db").cursor()
        username = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if db.execute("SELECT * FROM users WHERE user = ?", (username,)).fetchone():
            db.close()
            return render_template("register.html", error="Email already exists")
        
        if not username:
            return render_template("register.html", error="Please enter a email")
        elif not password:
            return render_template("register.html", error="Please enter a password")
        elif len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters")
        elif password != password_confirm:
            return render_template("register.html", error="Passwords do not match")
        else:
            db.execute("INSERT INTO users (user, hash) VALUES (?, ?)", (username, generate_password_hash(password,method='pbkdf2', salt_length=16)))
            db.connection.commit()
            db.close()
            return "posting"
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_name")
    session.pop("user_id")
    return redirect("/")

@app.route("/search", methods=["POST"])
@login_required
def search():
    db = sqlite3.connect("songs.db").cursor()
    search = request.form.get("search")

    query = "SELECT * FROM songs WHERE artist LIKE ? OR album LIKE ? LIMIT 15"
    db.execute(query,('%' + search + '%','%' + search + '%',))
    search_results = db.fetchall()
    db.close()

    if search == "":
        search_results = []

    return render_template("search.html",search_results=search_results)

@app.route("/catalogue")
@login_required
def catalogue():
    db = sqlite3.connect("songs.db").cursor()
    db.execute("SELECT * FROM songs ORDER BY RANDOM() LIMIT 18")
    songs = db.fetchall()
    db.close()
    return render_template("catalogue.html", songs=songs)

@app.route("/item")
@login_required
def item():
    db = sqlite3.connect("songs.db").cursor()
    album_id = request.args.get("q",'')
    db.execute("SELECT * FROM songs WHERE id = ?",(album_id,))
    data = db.fetchall()
    print(data[0][0])
    db.close()
    return render_template("item.html",data=data)

@app.route("/close")
@login_required
def close():
    return ""

@app.route("/manage_basket")
def manage_basket():

    action = request.args.get("action")
    item_id = request.args.get("id")

    if 'basket' not in session:
        session['basket'] = {}

    basket_list = session['basket']

    try:
        basket_list[item_id] += 1
    except:
        basket_list[item_id] = 1

    session['basket'] = basket_list
    print(session)

    # Check if user has active basket
    # db = sqlite3.connect("songs.db")
    # cursor = db.cursor()
    # user_id = int(session['user_id'])
    # cursor.execute("SELECT * FROM orders")
    # query = cursor.fetchall()
    # print(query)

    # cursor.execute("SELECT order_id FROM orders WHERE status = 'new' AND user_id = ?",(user_id,))
    # query = cursor.fetchall()
    # print(query)

    # if query:
    #     order_id = query[0][0]
    # else:
    #     cursor.execute("INSERT INTO orders(user_id,status) VALUES (?,'new')",(user_id,))
    #     db.commit()
    #     cursor.execute("SELECT order_id FROM orders WHERE status = 'new' AND user_id = ?",(user_id,))
    #     query = cursor.fetchall()
    #     print(query)
    #     order_id = query[0][0]
    # print(order_id)
    # db.close()

    return ""



if __name__ == "__main__":
    app.run(debug=True)

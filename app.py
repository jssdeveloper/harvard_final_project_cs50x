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
            

            session['user_id'] = db.execute("SELECT * FROM users WHERE user = ?", (username,)).fetchone()[0]
            session['user_name'] = username

            db.close()
            return redirect("/")
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
    db.close()
    return render_template("item.html",data=data)

@app.route("/close")
@login_required
def close():
    return ""

@app.route("/basket")
@login_required
def basket():
    
    # if len(session['basket']) <1 or 'basket' not in session:
    #     message = "Cart Empty"
    #     return render_template("basket.html",message=message)

    try:
        db = sqlite3.connect("songs.db").cursor()
        basket_list = session['basket']
        basket_items = []
        for item in basket_list:
            db.execute("SELECT * FROM songs WHERE id = ?",(item,))
            basket_items.append({"album":db.fetchall()[0], "quantity":basket_list[item]})
        db.close()
        basket_total = 0
        for item in basket_items:
            basket_total += float(item['album'][8]) * int(item['quantity'])
        return render_template("basket.html",basket_items=basket_items, basket_total=basket_total)
    except:
        message = "Cart Empty"
        return render_template("basket.html",message=message)

@app.route("/manage_basket")
def manage_basket():

    action = request.args.get("action")
    item_id = request.args.get("id")

    if action == "add":

        if 'basket' not in session:
            session['basket'] = {}

        basket_list = session['basket']

        try:
            basket_list[item_id] += 1
        except:
            basket_list[item_id] = 1

        session['basket'] = basket_list

        return ''
    
    elif action == "remove":
        basket_list = session['basket']
        del basket_list[item_id]
        session['basket'] = basket_list

        return redirect(url_for('basket'))

@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    if request.method == "POST":
        basket_list = session['basket']

         # Check if user has active basket
        db = sqlite3.connect("songs.db")
        cursor = db.cursor()
        user_id = (session['user_id'])
        cursor.execute("SELECT order_id FROM orders WHERE status = 'new' AND user_id = ?",(user_id,))
        query = cursor.fetchall()
        
        if query:
            order_id = query[0][0]
        else:
            cursor.execute("INSERT INTO orders(user_id,status) VALUES (?,'new')",(user_id,))
            db.commit()
            cursor.execute("SELECT order_id FROM orders WHERE status = 'new' AND user_id = ?",(user_id,))
            query = cursor.fetchall()
            order_id = query[0][0]

        total = 0 
        for item in basket_list:
            cursor.execute("SELECT price FROM songs WHERE id = ?",(item,))
            price = cursor.fetchall()[0][0]
            total += price * basket_list[item]
  
        cursor.execute("UPDATE orders SET status = 'done', total = ? WHERE order_id = ?",(total,order_id,))
        db.commit()

        for item in basket_list:
            cursor.execute("SELECT price FROM songs WHERE id = ?",(item,))
            price = cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO order_item(order_id, record_id, quantity, price) VALUES (?,?,?,?)",(order_id,item,session["basket"][item],price,))
            db.commit()

        db.close()

        session['basket'] = {}

        return """<p class="text-xl mt-2 font-bold text-center">Checkout completed!</p>"""

@app.route("/profile")
@login_required
def profile():
    db = sqlite3.connect("songs.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM orders JOIN order_item ON order_item.order_id = orders.order_id WHERE user_id = ? ",(session['user_id'],))
    orders = cursor.fetchall()

    data = []

    for order in orders:
        songs_id = order[6]
        cursor.execute("SELECT * FROM songs WHERE id = ?",(songs_id,))
        query = cursor.fetchall()
        artist = query[0][1]
        album = query[0][2]
        image = query[0][4]
        price = order[8]
        qty = order[7]

        data.append({"artist":artist,"album":album,"image":image,"price":price,"qty":qty})
    
    db.close()
    return render_template("profile.html",data=data, username=session['user_name'])

@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        repeat_password = request.form.get("repeat_password")

        if not current_password:
            return "Please enter your current password"

        db = sqlite3.connect("songs.db")
        cursor = db.cursor()
        cursor.execute("SELECT hash FROM users WHERE id = ?",(session['user_id'],))
        query = cursor.fetchall()
        db.close()

        if not check_password_hash(query[0][0], current_password): 
            return "Incorrect password"
        else:
            if new_password != repeat_password:
                return "Passwords do not match"
            else:
                db = sqlite3.connect("songs.db")
                cursor = db.cursor()
                cursor.execute("UPDATE users SET hash = ? WHERE id = ?",(generate_password_hash(new_password,method='pbkdf2', salt_length=16),session['user_id'],))
                db.commit()
                db.close()
                return "Password changed successfully"

if __name__ == "__main__":
    app.run(debug=True)






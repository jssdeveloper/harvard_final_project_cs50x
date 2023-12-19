from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
app = Flask(__name__)
app.config["SESSION_TIMEOUT"] = 3600
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
    return "index"

@app.route("/login", methods=["GET", "POST"])
def login():
    return "login"

@app.route("/logout")
def logout():
    return "logout"

if __name__ == "__main__":
    app.run(debug=True)

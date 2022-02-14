from flask import Flask, render_template, request
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine("sqlite:///paypalme.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["user"]
    password = request.form["password"]

    login_query = f"""
    SELECT id, username
    FROM users
    WHERE username='{username}' and password='{password}'
    """

    with engine.connect() as connection:
        user = connection.execute(login_query).fetchone()

        if user:
            return render_template("private.html", user=user)
        else:
            return render_template("unauthorized.html"), 403


app.run(debug=True)
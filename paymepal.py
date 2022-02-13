from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine("sqlite:///paypalme.db")

@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True)
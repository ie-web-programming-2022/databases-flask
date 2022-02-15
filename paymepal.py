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
    WHERE username='{username}' AND password='{password}'
    """

    transactions_query = f"""
    SELECT transactions.amount, transactions.currency, shops.name
    FROM transactions
    INNER JOIN users ON transactions.user_id=users.id
    INNER JOIN shops ON transactions.shop_id=shops.id
    WHERE username='{username}'
    ORDER BY transactions.timestamp
    """

    with engine.connect() as connection:
        user = connection.execute(login_query).fetchone()

        if user:
            transactions = connection.execute(transactions_query).fetchall()
            return render_template("private.html", user=user, transactions=transactions)
        else:
            return render_template("unauthorized.html"), 403


app.run(debug=True)
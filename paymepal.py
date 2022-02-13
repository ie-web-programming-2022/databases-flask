from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine("sqlite:///paypalme.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/insert", methods=["POST"])
def insert():
    amount = request.form["amount"]
    shop = request.form["shop"]
    username = request.form["username"]

    users_query = f"""
    SELECT id
    FROM users
    WHERE username='{username}'
    """

    shops_query = f"""
    SELECT id
    FROM shops
    WHERE name='{shop}'
    """


    with engine.connect() as connection:
        user = connection.execute(users_query).fetchone()
        shop = connection.execute(shops_query).fetchone()

        insert_query = f"""
        INSERT INTO transactions (user_id, amount, currency, timestamp, shop_id)
        VALUES ({user[0]}, {amount}, "EUR", "14/02/2022", {shop[0]})
        """
        connection.execute(insert_query)

        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["user"]
    password = request.form["password"]

    login_query = f"""
    SELECT *
    FROM USERS
    WHERE username='{username}'
    AND password='{password}'
    """

    transactions_query = f"""
    SELECT t.amount, t.currency, s.name
    FROM transactions t
    INNER JOIN users u ON t.user_id=u.id
    INNER JOIN shops s ON t.shop_id=s.id
    WHERE u.username='{username}'
    """

    with engine.connect() as connection:
        user = connection.execute(login_query).fetchone()
        transactions = connection.execute(transactions_query).fetchall()

        return render_template("private.html", user=user, transactions=transactions)

    #return "implement the queries"

app.run(debug=True)
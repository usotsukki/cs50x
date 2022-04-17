import os

from cs50 import SQL
from flask import Flask, flash, helpers, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy.sql.base import Executable
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import sqlite3


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:/finance.db")


# some global variables
gbquantity = 0
gbtotal = 0
gstocks = 0
gstonk = 0

gsquantity = 0
gstotal = 0


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


##################################### HOME ########################################
##################################### HOME ########################################


@ app.route("/", methods=["GET", "POST"])
@ login_required
def index():
    if request.method == "POST":
        if request.form.get("rel") == "rell":
            return redirect("/rel_index")
        else:
            return redirect("/")
    else:
        """Show portfolio of stocks"""
        name = db.execute(
            "select username from users where id = ?", session["user_id"])[0]["username"]
        portfolio = db.execute(
            "select * from users where id = ?", session["user_id"])
        del portfolio[0]["hash"]
        del portfolio[0]["id"]
        del portfolio[0]["username"]
        values = []
        prices = []
        total = 0
        for i in portfolio[0]:
            if not (i == 'cash'):
                price = db.execute(
                    "select price from stocks where symbol = ?", i)
                value = (price[0]["price"]) * (int(portfolio[0][i]))
                prc = price[0]["price"]

            else:
                value = float(portfolio[0][i])
                prc = 1

            prices.append(prc)
            values.append(value)
            total += value

        return render_template("index.html", name=name, portfolio=portfolio, values=values, prices=prices, total=total)


#################################### FULL UPDATE ###################################
#################################### FULL UPDATE ###################################


@ app.route("/rel_index", methods=["GET", "POST"])
@ login_required
def rel_index():
    """Show portfolio of stocks"""
    name = db.execute(
        "select username from users where id = ?", session["user_id"])[0]["username"]
    portfolio = db.execute(
        "select * from users where id = ?", session["user_id"])
    del portfolio[0]["hash"]
    del portfolio[0]["id"]
    del portfolio[0]["username"]
    values = []
    prices = []
    total = 0
    for i in portfolio[0]:
        if not i == 'cash' and int(portfolio[0][i]) > 0:
            up_stonk = lookup(i)
            up_string_qr = "update stocks set price = %f where symbol = %s" % (
                up_stonk["price"], "'" + up_stonk["symbol"] + "'")
            db.execute(up_string_qr)
    # updated portfolio
    portfolio = db.execute(
        "select * from users where id = ?", session["user_id"])
    del portfolio[0]["hash"]
    del portfolio[0]["id"]
    del portfolio[0]["username"]
    for i in portfolio[0]:
        if not i == 'cash':
            price = db.execute(
                "select price from stocks where symbol = ?", i)
            value = (price[0]["price"]) * (int(portfolio[0][i]))
            prc = price[0]["price"]

        else:
            value = float(portfolio[0][i])
            prc = 1

        prices.append(prc)
        values.append(value)
        total += value

    return render_template("index.html", name=name, portfolio=portfolio, values=values, prices=prices, total=total)


###################################### QUOTE ######################################
###################################### QUOTE ######################################


@ app.route("/quote", methods=["GET", "POST"])
@ login_required
def quote():

    if request.method == "POST":
        smbl = request.form.get("symbol")
        stonk = lookup(smbl)
        # if such stock exists
        if stonk:
            # check if stock is in db, if it is replace it with newer info
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            if len(stocks) > 0:
                db.execute("delete from stocks where name = ?", stonk["name"])
            db.execute("insert into stocks(name, price, symbol) values(?, ?, ?)",
                       stonk["name"], stonk["price"], stonk["symbol"])
            # add stock clumn to users db if needed (to store trading data)
            cursor = db.execute('select * from users')  # outputs list of dict

            if stonk["symbol"] not in cursor[0]:
                db.execute(
                    "alter table users add column ? integer not null default 0", stonk["symbol"])

            # display stock info on client side
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            return render_template("quote.html", stocks=stocks)
        # if stock does not exist
        else:
            return apology("no such stock(")
    else:
        return render_template("quote.html")


###################################### BUY ######################################
###################################### BUY ######################################


@ app.route("/buy", methods=["GET", "POST"])
@ login_required
def buy():
    if request.method == 'POST':
        smbl = request.form.get("symbol")
        bquantity = request.form.get("quantity")
        if not bquantity.isdigit():
            return apology("not valid request")
        elif float(bquantity) < 1:
            return apology("not valid request")
        stonk = lookup(smbl)
        global gstonk
        gstonk = stonk
        # if such stock exists
        if stonk:
            # check if stock is in db, if it is replace it with newer info
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            if len(stocks) > 0:
                db.execute("update stocks set price = ? where name = ?",
                           stonk["price"], stonk["name"])
            else:
                db.execute("insert into stocks(name, price, symbol) values(?, ?, ?)",
                           stonk["name"], stonk["price"], stonk["symbol"])
            # add stock column to users db if needed (to store trading data)
            cursor = db.execute('select * from users')  # outputs list of dict

            if stonk["symbol"] not in cursor[0]:
                db.execute(
                    "alter table users add column ? integer not null default 0", stonk["symbol"])

            # display stock info on client side
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            btotal = stonk["price"] * float(bquantity)
            global gstocks
            gstocks = stocks
            global gbtotal
            gbtotal = btotal
            global gbquantity
            gbquantity = bquantity

            return render_template("confbuy.html", stocks=stocks, total=btotal, quantity=bquantity)
        # if stock does not exist
        else:
            return apology("no such stock(")
    else:
        return render_template("buy.html")


@ app.route("/confbuy", methods=["GET", "POST"])
@ login_required
def confbuy():
    if request.method == "POST":
        id = session["user_id"]

        # select stock from user portfolio to update
        get_quan_from_portfolio = (
            "select %s from users where id = %d" % (gstonk['symbol'], id))
        sq = db.execute(get_quan_from_portfolio)[0][gstonk['symbol']]
        fsq = sq + int(gbquantity)
        svalue = fsq * gstonk["price"]
        # select cash to check if order is valid
        get_quan_from_portfolio = (
            "select %s from users where id = %d" % ('cash', id))
        cq = float(db.execute(get_quan_from_portfolio)[0]['cash'])
        fcq = cq - float(gbtotal)

        if fcq > -0.001:

            update_portfolio = (
                "update users set %s = %d where id = %d" % (gstonk["symbol"], fsq, id))
            db.execute(update_portfolio)
            update_cash = (
                "update users set %s = %d where id = %d" % ("cash", fcq, id))
            db.execute(update_cash)
            commission_p = commission_motherfucker(gbtotal)
            update_history('buy', gstonk['symbol'],
                           gbquantity, gstonk["price"], gbtotal, svalue, commission_p)
        else:
            return apology("You're to broke for this operation")

        return index()
    else:
        return apology('What are You doing?')


###################################### SELL ######################################
###################################### SELL ######################################


@ app.route("/sell", methods=["GET", "POST"])
@ login_required
def sell():
    if request.method == 'POST':
        smbl = request.form.get("symbol")
        squantity = request.form.get("quantity")
        if not squantity.isdigit():
            return apology("not valid request")
        elif float(squantity) < 1:
            return apology("not valid request")
        stonk = lookup(smbl)
        global gstonk
        gstonk = stonk
        # if such stock exists
        if stonk:
            # check if stock is in db, if it is replace it with newer info
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            if len(stocks) > 0:
                db.execute("update stocks set price = ? where name = ?",
                           stonk["price"], stonk["name"])
            else:
                db.execute("insert into stocks(name, price, symbol) values(?, ?, ?)",
                           stonk["name"], stonk["price"], stonk["symbol"])
            # add stock column to users db if needed (to store trading data)
            cursor = db.execute('select * from users')  # outputs list of dict

            if stonk["symbol"] not in cursor[0]:
                db.execute(
                    "alter table users add column ? integer not null default 0", stonk["symbol"])

            # display stock info on client side
            stocks = db.execute(
                "select * from stocks where name = ?", stonk["name"])
            stotal = stonk["price"] * float(squantity)
            global gstocks
            gstocks = stocks
            global gstotal
            gstotal = stotal
            global gsquantity
            gsquantity = squantity

            return render_template("confsell.html", stocks=stocks, total=stotal, quantity=squantity)
        # if stock does not exist
        else:
            return apology("no such stock(")
    else:
        return render_template("sell.html")


@ app.route("/confsell", methods=["GET", "POST"])
@ login_required
def confsell():
    if request.method == "POST":
        id = session["user_id"]

        # select stock from user portfolio to update and then check if user has enough for operation
        get_quan_from_portfolio = (
            "select %s from users where id = %d" % (gstonk['symbol'], id))
        sq = db.execute(get_quan_from_portfolio)[0][gstonk['symbol']]
        fsqs = sq - int(gsquantity)
        svalues = fsqs * gstonk["price"]
        # select cash to check if order is valid
        get_quan_from_portfolio = (
            "select %s from users where id = %d" % ('cash', id))
        cq = float(db.execute(get_quan_from_portfolio)[0]['cash'])
        fcq = cq + float(gstotal)

        if fsqs > -0.001:

            update_portfolio = (
                "update users set %s = %d where id = %d" % (gstonk["symbol"], fsqs, id))
            db.execute(update_portfolio)
            update_cash = (
                "update users set %s = %d where id = %d" % ("cash", fcq, id))
            db.execute(update_cash)
            commission_p = commission_motherfucker(gstotal)
            update_history('sell', gstonk['symbol'],
                           gsquantity, gstonk["price"], gstotal, svalues, commission_p)
        else:
            return apology("You don't have enough shares for this operation")

        return index()
    else:
        return apology('What happend?')


#################################### HISTORY ####################################
#################################### HISTORY ####################################


@ app.route("/history")
@ login_required
def history():

    # transaction history
    history = db.execute(
        "select * from history where user_id = ?", session["user_id"])

    # commission history (admin only)
    if session["user_id"] == 1:
        adm_history = db.execute("select * from commission_history")
    else:
        adm_history = [0]

    if len(history) > 0:
        del history[0]["id"]

        return render_template("history.html", history=history, adm_history=adm_history)
    else:
        return apology("your history is empty")


################################### REGISTER ###################################
################################### REGISTER ###################################


@ app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confpassword = request.form.get("confpassword")
        hash = generate_password_hash(request.form.get("password"))
        rows = db.execute("select * from users where username = ?", (name))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif int(len(rows)) > 0:
            return apology("username taken", 403)
        elif not password == confpassword:
            return apology("passwords don't match")

        else:

            db.execute(
                "insert into users(username, hash) values(?, ?)", name, hash)
            return redirect("/")

    else:
        return render_template("register.html")


##################################### LOGIN #####################################
##################################### LOGIN #####################################


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


#################################### LOGOUT ####################################
#################################### LOGOUT ####################################


@ app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


#################################### HELPERS ###################################
#################################### HELPERS ###################################


# updates history for BUY and SELL via single fuction call
def update_history(operation, symbol, quantity, price, total, value, commission):

    # get current date&time string
    now = datetime.now()
    dt_string = (("'") + (now.strftime("%d/%m/%Y %H:%M:%S")) + ("'"))

    operation = (("'") + (operation) + ("'"))
    symbol = (("'") + (symbol) + ("'"))
    user_id = session["user_id"]

    query_str = "insert into history(date, operation, symbol, quantity, price, total, value, user_id, commission) values(%s, %s, %s, %d, %f, %f, %f, %d, %f)" % (
        dt_string, operation, symbol, int(quantity), price, total, value, int(user_id), commission)

    query_str_adm = "insert into commission_history(user_id, date, operation, symbol, total, commission) values(%d, %s, %s, %s, %f, %f)" % (
        int(user_id), dt_string, operation, symbol, total, commission)

    db.execute(query_str)
    db.execute(query_str_adm)


# We’re taking home cold hard cash via commission, motherfucker.
def commission_motherfucker(amount):
    commission_amount = amount * 0.0025
    commission_query_ac = "select cash from users where username = 'admin'"
    commission_query_uc = "select cash from users where id = %s" % (
        session["user_id"])

    usr_cash = float(db.execute(commission_query_uc)[0]["cash"])
    upd_usr_cash = usr_cash - commission_amount
    commission_query_upd_usr_cash = "update users set cash = %f where id = %d" % (
        upd_usr_cash, session["user_id"])
    db.execute(commission_query_upd_usr_cash)

    adm_cash = float(db.execute(commission_query_ac)[0]["cash"])
    upd_adm_cash = adm_cash + commission_amount
    commission_query_upd_adm_cash = "update users set cash = %f where username = 'admin'" % (
        upd_adm_cash)
    db.execute(commission_query_upd_adm_cash)

    return commission_amount


if __name__ == "__main__":
    app.run(host="172.16.200.10", port=5050, debug=True)

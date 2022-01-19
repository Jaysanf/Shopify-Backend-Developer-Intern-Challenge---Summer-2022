from ast import iter_child_nodes
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3

from Item import Item
from helpers import create_connection, apology, tuple_to_dict, getInv


DB_PATH = 'inventory.db'
my_connection = create_connection(DB_PATH)

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        inventoryList = getInv(my_connection)
        
        return render_template("index.html", inventoryList=inventoryList)


@app.route("/create", methods=["POST"])
def create():
    if request.method == "POST":
        name=request.form.get("name") 
        quantity=request.form.get("quantity")
        if not name:
            return apology("must provide item name", 403)
        
        elif not quantity:
            return apology("must provide quantity", 403)
        item_to_add = Item((None,name,quantity))

        my_connection.execute("INSERT INTO inventory (ItemName, ItemQuantity) VALUES (:name, :quantity)", item_to_add.getItemDict() )

        inventoryList = getInv(my_connection)
        return render_template("index.html", inventoryList=inventoryList)

@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        item_id=request.form.get("id") 
        if not item_id:
            return apology("must provide item id", 403)
        

        my_connection.execute("DELETE FROM inventory where ItemID=:id", {'id':item_id} )

        inventoryList = getInv(my_connection)
        return render_template("index.html", inventoryList=inventoryList)

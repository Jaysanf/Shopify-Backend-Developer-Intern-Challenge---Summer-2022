from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3

from Item import Item
from helpers import create_connection, apology, tuple_to_dict


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
        inventoryCursor = my_connection.execute("SELECT * FROM inventory")
        inventoryList = inventoryCursor.fetchall()
        inventoryList = tuple_to_dict(inventoryList)
        

        return render_template("index.html", inventoryList=inventoryList)

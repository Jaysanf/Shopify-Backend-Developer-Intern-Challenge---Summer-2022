
from flask import Flask, render_template, request, send_file
from flask_session import Session
from tempfile import mkdtemp

from Item import Item
from helpers import create_connection, apology, getInv, getItemObj, getMemObj




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
        my_connection.commit()

        inventoryList = getInv(my_connection)
        return render_template("index.html", inventoryList=inventoryList)

@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        item_id=request.form.get("id") 
        if not item_id:
            return apology("must provide item id", 403)
        

        my_connection.execute("DELETE FROM inventory where ItemID=:id", {'id':item_id} )
        my_connection.commit()
        inventoryList = getInv(my_connection)
        return render_template("index.html", inventoryList=inventoryList)


@app.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "GET":
        item_id=request.args['id'] 

        if not item_id:
            return apology("must provide item id", 403)

        inventoryList = getInv(my_connection)
        item_to_edit = getItemObj(inventoryList, int(item_id))

        return render_template("edit.html", item_to_edit=item_to_edit)
    
    elif request.method == "POST":
        item_id=request.form.get("id")
        name=request.form.get("name") 
        quantity=request.form.get("quantity")

        if not item_id:
            return apology("must provide item id", 403)
        if not name:
            return apology("must provide item name", 403)
        elif not quantity:
            return apology("must provide quantity", 403)
        
        item_to_edit = Item((item_id,name,quantity))
        my_connection.execute("UPDATE inventory SET ItemName=:name, ItemQuantity=:quantity WHERE ItemId=:id", item_to_edit.getItemDict() )
        my_connection.commit()

        inventoryList = getInv(my_connection)
        return render_template("index.html", inventoryList=inventoryList)


@app.route("/export", methods=["POST"])
def export():
    if request.method == "POST":
        mem = getMemObj(my_connection)
        return send_file(mem,
                    mimetype='text/csv',
                    attachment_filename='MyInventory.csv',
                    as_attachment=True)
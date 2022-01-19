
from csv import DictWriter
import sqlite3
from typing import Dict, Tuple
from flask import  render_template
from io import StringIO, BytesIO

from Item import Item



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def create_connection(path: str):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print("Connection successful")
    
    except sqlite3.Error as e:
        print(f"The error : '{e}' occured.")

    return connection

def tuple_to_dict(inventoryList: list[Tuple])-> list[Dict]:
    for i in range(len(inventoryList)):
            item = inventoryList[i]
            myItem = Item(item)
            inventoryList[i] = myItem.getItemDict()
    return inventoryList

def getInv(connection) -> list[Dict]:
    inventoryCursor = connection.execute("SELECT * FROM inventory")
    inventoryList = inventoryCursor.fetchall()
    inventoryList = tuple_to_dict(inventoryList)
    return inventoryList

def getItemObj(inventory:list[Dict], id:int) -> Item:
    for item in inventory:
        if item['id'] == id:
            return Item((item['id'],item['name'],item['quantity']))
    else:
        return None

def getMemObj(connection):
    fieldnames = ['id','name','quantity']
    proxy = StringIO()


    writer = DictWriter(proxy,fieldnames=fieldnames)
    writer.writeheader()
    inventory = getInv(connection)
    writer.writerows(inventory)
    mem = BytesIO()
    mem.write(proxy.getvalue().encode())
    # seeking was necessary. Python 3.5.2, Flask 0.12.2
    mem.seek(0)
    proxy.close()
    return mem
        
        




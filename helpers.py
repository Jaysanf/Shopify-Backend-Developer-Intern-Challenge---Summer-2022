
import imp
import sqlite3
from typing import Dict, Tuple
from flask import  render_template

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





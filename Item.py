from typing import Tuple


class Item:
    
    def __init__(self, item: Tuple) -> None:
        self.id = item[0]
        self.name = item[1]
        self.quantity = item[2]

    def getItemDict(self) -> Tuple:
        return {"id":self.id, "name":self.name, "quantity":self.quantity}
import krait_util

class KRAITQueue:
    def __init__(self, name: str) -> None:
        self.name = name
        self.items = []

    def push(self, item: str):
        self.items.append(item)
        return len(self.items) - 1

    def pop(self, item_number: int = -1):
        if len(self.items) > 0:
            pos = item_number
            if pos < 0:
                pos = len(self.items) - 1
            return self.items.pop(pos)
        return krait_util.EMPTY_STRING
    
    
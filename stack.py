class Stack:
    def __init__(self, max_size=5):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
        else:
            raise Exception("Stack Overflow")

    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            raise Exception("Stack Underflow")

    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
class Stack:

    def __init__(self):
        self.items = []

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

    def is_empty(self):
        return self.items == []

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items) - 1]

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def push(self, value):
        self.items.append(value)

    def size(self):
        return len(self.items)


def is_balanced(input_brackets):
    expected_brackets_stack = Stack()
    brackets_mapping = dict(zip('([{', ')]}'))

    for bracket in input_brackets:
        if bracket in brackets_mapping:
            expected_brackets_stack.push(brackets_mapping[bracket])
        else:
            if expected_brackets_stack.is_empty() or bracket != expected_brackets_stack.pop():
                return 'Unbalanced'
    return 'Balanced'


brackets = '[[{())}]'
print(is_balanced(brackets))

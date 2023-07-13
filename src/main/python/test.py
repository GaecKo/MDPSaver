class Control:
    def __init__(self):
        self.name = "hello"

    def getVal(self):
        return self.name

    def print_smth(self):
        print("Hello")


class Uses(Control):
    def __init__(self):
        super().__init__()
        print(self.getVal())

me = Uses()
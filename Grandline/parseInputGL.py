

class Parse_input:
    def __init__(self, path):
        self.path = path
        with open(self.path) as file:
            input_arr = file.readlines()
            input_arr = [line.rstrip() for line in input_arr]
        return input_arr


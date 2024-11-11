class EPCCodeGenerator:
    def __init__(self):
        self.counter = 0

    def generate_code(self):
        self.counter += 1
        return f"CY{str(self.counter).zfill(3)}"
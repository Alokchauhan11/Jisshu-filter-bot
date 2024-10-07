class InvalidHash(Exception):
    def __init__(self, message="Invalid hash"):
        self.message = message
        super().__init__(self.message)

class FileNotFound(Exception):
    def __init__(self, message="File not found"):
        self.message = message
        super().__init__(self.message)

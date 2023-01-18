class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class InternalException(Exception):
    def __init__(self, message: str, status: int, name: str):
        self.name = name
        self.message = message
        self.status = status
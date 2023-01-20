class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class InternalException(Exception):
    def __init__(self, message: str = None,  name: str = None, status: int = 500,):
        self.name = name
        self.message = message
        self.status = status
        
class UnauthorizedException(Exception):
    def __init__(self, message: str = None, name: str = None,):
        self.message = message if name == None else name

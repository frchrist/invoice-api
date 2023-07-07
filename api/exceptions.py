

class InvoiceObjectNotFound(Exception):
    def __init__(self,message, code=None) -> None:
        self.message = message
        self.code = code
        super().__init__(message)



class ClientObjectNotFound(Exception):
    def __init__(self,message, code=None) -> None:
        self.message = message
        self.code = code

        super().__init__(message)

"""Define general response"""


class Response:
    """Response"""

    def __init__(self, code=0, data=None, msg=""):
        self.code = code
        self.data = data
        self.msg = msg

    def as_dict(self):
        """as_dict

        serialize Response
        """

        return {name: getattr(self, name)
                for name in dir(self)
                if not name.startswith("__") and not callable(getattr(self, name))}


class RequestErrorResponse(Response):
    """RequestErrorResponse"""

    code = 1

    def __init__(self, msg=""):
        super().__init__()
        self.msg = msg
        self.code = 1

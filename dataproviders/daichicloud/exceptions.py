class DaichiCloudException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DaichiCloudCommandException(DaichiCloudException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DaichiCloudHttpException(Exception):
    def __init__(self, message: str, code: int):
        """
            Base HTTP error
        """
        self.code = code
        super().__init__(message)

    def __str__(self):
        if self.code:
            return f"{self.args[0]} (error code: {self.code})"
        return self.args[0]

class DaichiCloudServerProblemException(DaichiCloudHttpException):
    def __init__(self, message: str, code: int):
        """
        Server has problem 500, 503, 504

        :param message: error message
        :param code: error http code
        """
        super().__init__(message=message, code=code)

class DaichiCloudAuthErrorException(DaichiCloudHttpException):
    def __init__(self, message: str, code: int):
        """
        Incorrect token/login or password

        :param message: error message
        :param code: error http code
        """
        super().__init__(message=message, code=code)


class DaichiCloudUnknowErrorException(DaichiCloudHttpException):
    def __init__(self, message: str, code: int):
        """
        Unknown Error

        :param message: error message
        :param code: error http code
        """
        super().__init__(message=message, code=code)


class DaichiCloudException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DaichiCloudApiException(Exception):
    def __init__(self, message, code=None):
        """
        Пользовательское исключение для Daikin Cloud API

        :param message: Текст ошибки
        :param code: Код ошибки (опционально)
        """
        super().__init__(message)
        self.code = code

    def __str__(self):
        if self.code:
            return f"{self.args[0]} (error code: {self.code})"
        return self.args[0]

class CliArgumentsError(Exception):
    def __init__(self, user_argsv, message="Error en los argumentos"):
        self.user_argsv = user_argsv
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.user_argsv} -> {self.message}'


class CliUserNameError(Exception):
    def __init__(self, username, message="Error en el username"):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.username} -> {self.message}'

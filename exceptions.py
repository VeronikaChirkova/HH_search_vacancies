class EnvNotFoundError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class NeedAuthOnHHError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class NeedStopProgramError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

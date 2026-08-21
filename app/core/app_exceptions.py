class AppException(Exception):
    def __init__(self, status_code, message, error=None):
        self.status_code = status_code
        self.message = message
        self.error = error if error is not None else message

class DuplicatedEntryError(Exception):
    pass


class UserNotFoundException(Exception):
    def __init__(self, value):
        self.value = value


class InvalidPasswordException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UserLogoutException(Exception):
    pass


class CredentialsValidationException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class RequestProcessingException(Exception):
    pass


class InvalidRoleException(Exception):
    def __init__(self, value):
        self.value = value


class InvalidPermissionsException(Exception):
    pass

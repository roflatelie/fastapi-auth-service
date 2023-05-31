from fastapi import Request, Response, status, FastAPI
from fastapi.responses import JSONResponse

from src.core.exceptions import DuplicatedEntryError, InvalidPasswordException, \
    UserNotFoundException, CredentialsValidationException, InvalidTokenException, RequestProcessingException, \
    InvalidRoleException, InvalidPermissionsException


async def duplicate_entity_exception_handler(request: Request, exc: DuplicatedEntryError) -> Response:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "A user with this data already exists."}
    )


async def invalid_password_exception_handler(request: Request, exc: InvalidPasswordException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Incorrect password."}
    )


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"There is no user with this data: {exc}"}
    )


async def credentials_validation_exception_handler(request: Request, exc: CredentialsValidationException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Can not validate your credentials."}
    )


async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid token."}
    )


async def request_processing_exception_handler(request: Request, exc: RequestProcessingException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Please try later."}
    )


async def invalid_role_exception_handler(request: Request, exc: InvalidRoleException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Role does not exist: {exc}."}
    )


async def invalid_permissions_exception_handler(request: Request, exc: InvalidPermissionsException) -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "Permission denied."}
    )


def include_app(app: FastAPI):
    app.add_exception_handler(DuplicatedEntryError, duplicate_entity_exception_handler)
    app.add_exception_handler(InvalidPasswordException, invalid_password_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(CredentialsValidationException, credentials_validation_exception_handler)
    app.add_exception_handler(InvalidTokenException, invalid_token_exception_handler)
    app.add_exception_handler(RequestProcessingException, request_processing_exception_handler)
    app.add_exception_handler(InvalidRoleException, invalid_role_exception_handler)
    app.add_exception_handler(InvalidPermissionsException, invalid_permissions_exception_handler)

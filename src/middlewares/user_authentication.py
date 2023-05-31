from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from src.dependencies.usecase_dependencies import get_verify_user_token_usecase
from src.domain.token import Token
from src.usecases.verify_user_token import VerifyUserTokenUsecase


async def check_access_token(credentials: HTTPBasicCredentials = Depends(HTTPBearer()),
                             verification_usecase: VerifyUserTokenUsecase = Depends(get_verify_user_token_usecase),) -> Token:
    response = await verification_usecase.verify_user_token(credentials.credentials)
    return response

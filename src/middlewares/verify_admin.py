from fastapi import Depends
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from src.dependencies.usecase_dependencies import get_verify_user_token_usecase
from src.usecases.verify_user_token import VerifyUserTokenUsecase


async def check_admin_token(credentials: HTTPBasicCredentials = Depends(HTTPBearer()),
                            verification_usecase: VerifyUserTokenUsecase = Depends(get_verify_user_token_usecase),) -> None:
    await verification_usecase.verify_admin_token(credentials.credentials)

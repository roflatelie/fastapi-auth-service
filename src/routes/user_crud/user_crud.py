import json
import os

from fastapi import APIRouter, Depends, status, Response, Security, Request
from fastapi_filter import FilterDepends
from fastapi_jwt import JwtAuthorizationCredentials, JwtRefreshBearer
from fastapi.responses import JSONResponse

from src.domain.token import Token
from src.filters.user_filter import UserFilter
from src.middlewares.user_authentication import check_access_token
from src.middlewares.verify_admin import check_admin_token
from src.usecases.get_filtered_users import FilterUsersUsecase
from src.usecases.reset_password import ResetPasswordUsecase
from src.usecases.select_user_by_uuid import SelectUserByUUIDUsecase
from src.usecases.send_password_recovery_email import ResetPasswordEmailUsecase
from src.usecases.send_verification_email import VerificationEmailUsecase
from src.usecases.user_logout import UserLogoutUsecase
from src.usecases.user_signup import UserSignUpUsecase

from src.routes.user_crud.controller import CreateUserRequest, CreateUserResponse, LoginUserRequest, \
    TokenResponse, ResetUserPasswordRequest, GetUserRequest

from src.dependencies.usecase_dependencies import get_user_registration_usecase, get_user_login_usecase, \
    get_verify_user_email_usecase, get_user_logout_usecase, get_reset_password_usecase, get_verification_email_usecase, \
    get_reset_password_email_usecase, get_select_user_by_uuid_usecase, get_filtered_users_usecase
from src.usecases.user_token import UserLoginUsecase
from src.usecases.verify_user_email import VerifyUserEmailUsecase

router = APIRouter(prefix='/users')


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def register_user(
        data: CreateUserRequest,
        user_usecase: UserSignUpUsecase = Depends(get_user_registration_usecase)
):
    await user_usecase.register_user(data)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(
        data: LoginUserRequest,
        user_usecase: UserLoginUsecase = Depends(get_user_login_usecase)
):
    tokens = await user_usecase.login_user(data)
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    response = Response(content=json.dumps({"access_token": access_token}))
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@router.post("/refresh/", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh(
        credentials: JwtAuthorizationCredentials = Security(JwtRefreshBearer(
            secret_key=os.environ.get("SECRET_KEY"),
            auto_error=False,)
        )
):
    access_token = UserLoginUsecase.generate_token(subject=credentials.subject, expire_time=30)
    refresh_token = UserLoginUsecase.generate_token(subject=credentials.subject, expire_time=480)

    response = Response(content=json.dumps({"access_token": access_token}))
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@router.get("/account/verify_email/", dependencies=[Depends(check_access_token)], status_code=status.HTTP_200_OK,
            response_model=None)
async def send_verification_email(payload: Token = Depends(check_access_token),
                                  verification_usecase: VerificationEmailUsecase = Depends(
                                      get_verification_email_usecase)):
    await verification_usecase.send_verification_email(user_id=payload.user_id, email=payload.email)


@router.get("/service/verify_email/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def verify_user_email(user_id: str, verify_user_email_usecase: VerifyUserEmailUsecase =
                            Depends(get_verify_user_email_usecase)):
    await verify_user_email_usecase.update_email_verification(user_id=user_id)


@router.delete("/logout/", dependencies=[Depends(check_access_token)], status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(request: Request, logout_usecase: UserLogoutUsecase = Depends(get_user_logout_usecase)):
    access_token = request.headers.get("Authorization").split(" ")[1]
    refresh_token = request.cookies.get("refresh_token")
    await logout_usecase.logout_user(access_token=access_token, refresh_token=refresh_token)


@router.get("/account/reset_password/", dependencies=[Depends(check_access_token)],
            status_code=status.HTTP_204_NO_CONTENT)
async def send_reset_password_email(payload: Token = Depends(check_access_token),
                                    verification_usecase: ResetPasswordEmailUsecase = Depends(
                                        get_reset_password_email_usecase)):
    await verification_usecase.send_password_reset_email(user_id=payload.user_id, email=payload.email)


@router.patch("/service/reset_password/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def reset_user_password(user_id: str, password: ResetUserPasswordRequest,
                              reset_password_usecase:ResetPasswordUsecase = Depends(get_reset_password_usecase)):
    await reset_password_usecase.update_password(user_id=user_id, password=password.password)


@router.get("/admin/get_user", dependencies=[Depends(check_admin_token)], status_code=status.HTTP_200_OK)
async def get_user_by_uuid(data: GetUserRequest,
                           select_user_by_uuid_usecase: SelectUserByUUIDUsecase = Depends(get_select_user_by_uuid_usecase)):
    user = await select_user_by_uuid_usecase.login_user(data.user_id)
    return JSONResponse(content=user)


@router.get("/admin/get_users/filter", status_code=status.HTTP_200_OK)
async def get_user_by_uuid(select_filtered_users_usecase: FilterUsersUsecase = Depends(get_filtered_users_usecase),
                           user_filter: UserFilter = FilterDepends(UserFilter)):
    return await select_filtered_users_usecase.get_filtered_users(user_filter)

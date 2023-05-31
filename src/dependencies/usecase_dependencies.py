from fastapi import Depends

from src.adapters.repositories.aws_ses_repository import AWSSesRepository
from src.adapters.repositories.redis_repository import RedisRepository
from src.core.config import get_settings
from src.core.settings import BaseAppSettings
from src.dependencies.database import get_session
from src.usecases.get_filtered_users import FilterUsersUsecase
from src.usecases.reset_password import ResetPasswordUsecase
from src.usecases.select_user_by_uuid import SelectUserByUUIDUsecase
from src.usecases.send_password_recovery_email import ResetPasswordEmailUsecase
from src.usecases.send_verification_email import VerificationEmailUsecase
from src.usecases.user_logout import UserLogoutUsecase
from src.usecases.user_signup import UserSignUpUsecase
from src.adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.usecases.user_token import UserLoginUsecase
from src.usecases.verify_user_email import VerifyUserEmailUsecase
from src.usecases.verify_user_token import VerifyUserTokenUsecase


def get_user_registration_usecase(session=Depends(get_session)):
    return UserSignUpUsecase(SQLAlchemyUserRepository(session))


def get_user_login_usecase(session=Depends(get_session)):
    return UserLoginUsecase(SQLAlchemyUserRepository(session))


def get_verification_email_usecase(settings: BaseAppSettings = Depends(get_settings)):
    aws_repository = AWSSesRepository(settings.get_aws_creds)
    return VerificationEmailUsecase(aws_repository)


def get_verify_user_email_usecase(session=Depends(get_session)):
    return VerifyUserEmailUsecase(SQLAlchemyUserRepository(session))


def get_user_logout_usecase():
    redis_repository = RedisRepository()
    return UserLogoutUsecase(redis_repository)


def get_reset_password_email_usecase(settings: BaseAppSettings = Depends(get_settings)):
    aws_repository = AWSSesRepository(settings.get_aws_creds)
    return ResetPasswordEmailUsecase(aws_repository)


def get_reset_password_usecase(session=Depends(get_session)):
    return ResetPasswordUsecase(SQLAlchemyUserRepository(session))


def get_verify_user_token_usecase():
    redis_repository = RedisRepository()
    return VerifyUserTokenUsecase(redis_repository)


def get_select_user_by_uuid_usecase(session=Depends(get_session)):
    return SelectUserByUUIDUsecase(SQLAlchemyUserRepository(session))


def get_filtered_users_usecase(session=Depends(get_session)):
    return FilterUsersUsecase(SQLAlchemyUserRepository(session))

import uuid
from typing import Any

from sqlalchemy import select, update, or_
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm import joinedload, subqueryload

from src.adapters.orm_engines.models import User as UserModel, Role
from src.core.exceptions import UserNotFoundException, DuplicatedEntryError, \
    RequestProcessingException, InvalidRoleException
from src.filters.user_filter import UserFilter
from src.ports.repositories.user_repository import UserRepository
from src.domain.user import User, UserForAdmin
from src.usecases.password_hash import get_password_hash


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    async def select_user(self, user: User) -> User:
        try:
            query = select(UserModel).options(joinedload(UserModel.role)).where(or_(UserModel.email == user.login,
                                                                                    UserModel.username == user.login,
                                                                                    UserModel.phone_number == user.login))
            result = await self.session.execute(query)
            user_db = result.scalars().first()
            role_names = [role.name for role in user_db.role]
            user = User(
                user_id=user_db.user_id,
                username=user_db.username,
                email=user_db.email,
                phone_number=user_db.phone_number,
                password=user_db.password,
                role=role_names
            )
            return user
        except AttributeError as e:
            raise UserNotFoundException(user.login)
        except Exception as e:
            raise RequestProcessingException

    async def save_user(self, user: User) -> UserModel:
        try:
            user_db = UserModel()
            self.session.add(user_db)
            msg = user_db
            user_id = uuid.uuid4()
            user_db.user_id = user_id
            user_db.username = user.username
            user_db.email = user.email
            user_db.phone_number = user.phone_number
            user_db.password = get_password_hash(user.password)

            result = await self.session.execute(select(Role).filter_by(name="User"))
            user_role = result.scalar()
            if user_role is None:
                raise InvalidRoleException(user_role)
            user_db.role.append(user_role)
            await self.session.commit()
            await self.session.refresh(user_db)
            return msg
        except IntegrityError as e:
            await self.session.rollback()
            raise DuplicatedEntryError
        except Exception as e:
            await self.session.rollback()
            raise RequestProcessingException

    async def update_user(self, user_id: str, column_name: str, value: Any) -> dict:
        try:
            query = update(UserModel).where(UserModel.user_id == user_id).values({column_name: value}).returning(
                UserModel)
            user = await self.session.execute(query)
            if user.fetchone() is None:
                raise IntegrityError
            await self.session.commit()
            await self.session.flush()
            return {"detail": "Updated"}
        except IntegrityError:
            await self.session.rollback()
            raise UserNotFoundException
        except Exception:
            await self.session.rollback()
            raise RequestProcessingException

    async def select_user_by_uuid(self, user_id: uuid.UUID) -> UserForAdmin:
        try:
            query = select(UserModel).options(joinedload(UserModel.role)).where(UserModel.user_id == user_id)
            result = await self.session.execute(query)
            user_db = result.scalars().first()
            role_names = [role.name for role in user_db.role]
            user = UserForAdmin(
                user_id=str(user_db.user_id),
                username=user_db.username,
                email=user_db.email,
                phone_number=user_db.phone_number,
                role=role_names
            )
            return user
        except AttributeError:
            raise UserNotFoundException(user_id)
        except DBAPIError:
            raise UserNotFoundException(user_id)
        except Exception:
            raise RequestProcessingException

    async def select_filtered_users(self, user_filter: UserFilter) -> list:
        # try:
            query = select(UserModel).options(subqueryload(UserModel.role))
            filtered_query = user_filter.filter(query)
            return await self.session.execute(filtered_query)
        # except AttributeError:
        #     raise UserNotFoundException("filters error")
        # except Exception:
        #     raise RequestProcessingException

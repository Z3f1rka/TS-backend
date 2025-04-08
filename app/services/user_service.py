from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from app.api.schemas import UserGetResponse
from app.api.schemas import UserUpdateParameters
from app.utils import create_token
from app.utils import verify_password
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def register(self, username: str, email: str, password: str):
        async with self.uow:
            user_id = await self.uow.users.add_user(username=username, email=email, password=password)
            access_token = create_token("access", user_id, "user")
            refresh_token = create_token("refresh", user_id, "user")
            await self.uow.commit()
            await self.uow.sessions.add_token(user_id=user_id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def login(self, email: str, password: str):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(email=email)
            except NoResultFound:
                raise HTTPException(400, "Пользователя не существует")
            if not verify_password(password, user.hashed_password):
                raise HTTPException(400, "Неправильный пароль")
            access_token = create_token("access", user.id, user.role)
            refresh_token = create_token("refresh", user.id, user.role)
            await self.uow.sessions.add_token(user_id=user.id, jwt=refresh_token)
            await self.uow.commit()
            return access_token, refresh_token

    async def get_me(self, token: str):
        if isinstance(token, dict):
            async with self.uow:
                user = await self.uow.users.find_one(id=int(token["sub"]))
                user = UserGetResponse.model_validate(user)
            return user
        else:
            raise HTTPException(400, "Не валидный токен")

    async def get_user_by(self, **criterion):
        async with self.uow:
            try:
                user = await self.uow.users.find_one(**criterion)
            except NoResultFound:
                raise HTTPException(400, "Такого пользователя не существует")
            return UserGetResponse.model_validate(user)

    async def refresh(self, token: str):
        if isinstance(token, dict):
            async with self.uow:
                user = await self.uow.users.find_one(id=int(token["sub"]))
                access_token = create_token("access", user.id, user.role)
            return access_token
        else:
            raise HTTPException(400, "Не валидный токен")

    async def update_user(self, id: int, user: UserUpdateParameters):
        async with self.uow:
            try:
                await self.uow.users.find_one(id=id)
            except Exception:
                raise HTTPException(400, "Такого пользователя не существует")
            await self.uow.users.update_user(id=id, username=user.username, email=user.email, avatar=user.avatar)
            await self.uow.commit()

    async def add_privelegy(self, id: int, tier: int):
        async with self.uow:
            try:
                await self.uow.users.find_one(id=id)
            except Exception:
                raise HTTPException(400, "Такого пользователя не существует")
            await self.uow.users.add_privelegy(id=id, tier=tier)
            await self.uow.commit()

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.models.user import User
from app.repositories.basic_repo import Repository
from app.utils import get_password_hash


class UserRepository(Repository):
    model = User

    async def add_user(self, username: str, email: str, password: str):
        try:
            result = await super().add_one(
                {"username": username, "email": email, "hashed_password": get_password_hash(password)},
            )
            return result.id
        except IntegrityError:
            raise HTTPException(400, "Пользователь уже существует")

    async def update_user(self, id: int, username: str, email: str, avatar: str | None = None):
        stmt = select(self.model).where(self.model.id == id)
        user = (await self.session.execute(stmt)).scalars().first()
        if not username:
            username = user.username
        else:
            stmt = select(self.model).where(self.model.username == username)
            if (await self.session.execute(stmt)).scalars().all() and username != user.username:
                raise HTTPException(400, "Пользователь с таким именем уже существует")
        if not email:
            email = user.email
        else:
            stmt = select(self.model).where(self.model.email == email)
            if (await self.session.execute(stmt)).scalars().all() and email != user.email:
                raise HTTPException(400, "Пользователь с такой почтой уже существует")
        if not avatar:
            avatar = user.avatar
        user.avatar = avatar
        user.username = username
        user.email = email
        self.session.add(user)

    async def add_privelegy(self, id: int, tier: int):
        stmt = select(self.model).where(self.model.id == id)
        user = (await self.session.execute(stmt)).scalars().first()
        user.role = "tier" + str(tier)
        self.session.add(user)

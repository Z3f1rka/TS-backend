from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from app.db import Favorites
from app.db import Object
from app.db import User, Feedback
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

    async def add_favorites(self, user_id: int, object_id: int):
        stmt = select(Object).where(Object.main_object_id == object_id)
        routes = (await self.session.execute(stmt)).scalars().first()
        if not routes:
            raise HTTPException(400, "У маршрута нет опубликованных версий")
        stmt = insert(Favorites).values(user_id=user_id, object_id=object_id)
        await self.session.execute(stmt)

    async def delete_favorite(self, user_id: int, object_id: int):
        stmt = select(Favorites).where(Favorites.user_id == user_id, Favorites.object_id == object_id)
        try:
            user_favorite = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise HTTPException(400, "Маршрут не находится в избранном")
        await self.session.delete(user_favorite)

    async def get_favorites(self, user_id: int):
        stmt = select(Favorites).where(Favorites.user_id == user_id)
        user_favorite = (await self.session.execute(stmt)).scalars().all()
        for i in user_favorite:
            stmt = select(Object).where(Object.main_object_id == i.object_id).order_by(
                Object.version.desc())
            object = (await self.session.execute(stmt)).scalars().first()
            i.object = object
        return user_favorite

    async def add_privelegy(self, id: int, tier: int):
        stmt = select(self.model).where(self.model.id == id)
        user = (await self.session.execute(stmt)).scalars().first()
        user.role = "tier" + str(tier)
        self.session.add(user)

    async def feedback(self, id: int, text: str, email: str):
        stmt = insert(Feedback).values(user_id=id, text=text, email=email)
        await self.session.execute(stmt)
        
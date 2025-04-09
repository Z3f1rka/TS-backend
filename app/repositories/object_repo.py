from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update

from app.db.models.object import Object
from app.repositories.basic_repo import Repository


class ObjectRepository(Repository):
    model = Object

    async def add_object(self, user_id: int, title: str):
        stmt = insert(self.model).values(**{"user_id": user_id, "title": title}).returning(self.model)
        object = await self.session.execute(stmt)
        object_id = object.scalar_one().id
        stmt = update(self.model).where(self.model.id == object_id).values(main_object_id=object_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return object_id

    async def update(self, title: str, id: int, user_id: int, file: dict | None = None):
        stmt = select(self.model).where(self.model.main_object_id == id).order_by(self.model.version.desc())
        object = await self.session.execute(stmt)
        object = object.scalars().first()
        version = object.version
        stmt = insert(self.model).values(**{"title": title,
                                            "file": file,
                                            "main_object_id": id,
                                            "user_id": user_id,
                                            "version": version + 1})
        await self.session.execute(stmt)
        await self.session.commit()

    async def find_by_main_object_id(self, object_id):
        stmt = select(self.model).where(self.model.main_object_id == object_id).order_by(self.model.version.desc())
        object = await self.session.execute(stmt)
        object = object.scalars().first()
        if not object:
            return
        return object

    async def find_all_by_main_object_id(self, object_id):
        stmt = select(self.model).where(self.model.main_object_id == object_id).order_by(self.model.version.desc())
        objects = await self.session.execute(stmt)
        objects = objects.scalars().all()
        return objects

    async def find_by_id_private(self, object_id: int):
        stmt = select(self.model).where(self.model.id == object_id)
        object = await self.session.execute(stmt)
        object = object.scalars().first()
        return object

    """async def find_by_id_public(self, object_id: int):
        stmt = select(self.model).where(self.model.id == object_id,
                                        self.model.status == "public")
        object = await self.session.execute(stmt)
        object = object.scalars().first()
        if not object:
            return
        stmt = select(Comment).where(Comment.object_id == object_id, Comment.type == "public")
        comments = await self.session.execute(stmt)
        comments = comments.scalars().all()
        if not comments:
            object.rating = 0
        else:
            comments = [(i.created_at, i.rating) for i in comments if i.rating > 0]
            object.rating = rating_calculation(comments)
        return object"""

    """async def find_all_public_objects(self):
        stmt = select(self.model).where(self.model.status == "public")
        object = await self.session.execute(stmt)
        object = object.scalars().all()
        return [i for i in object]"""

    async def find_all_user_objects(self, user_id):
        stmt = select(self.model.main_object_id).where(self.model.user_id == user_id).group_by(
            self.model.main_object_id)
        object_id = await self.session.execute(stmt)
        object_id = object_id.scalars().all()
        objects = []
        for id in object_id:
            stmt = select(self.model).where(self.model.main_object_id == id).order_by(self.model.version.desc())
            object = await self.session.execute(stmt)
            object = object.scalars().first()
            objects.append(object)
        return objects

    """async def find_all_user_public_objects(self, user_id):
        objects = await self.find_all_user_objects(user_id)
        for_return = []
        for object in objects:
            if object.status == 'public':
                for_return.append(object)
        return for_return"""

    async def change_status(self, id: int, status: str):
        stmt = select(self.model).where(self.model.id == id)
        object = await self.session.execute(stmt)
        object = object.scalars().first()
        object.status = status
        self.session.add(object)

from fastapi import HTTPException

from app.api.schemas.object_schemas import AllObjectReturn
from app.api.schemas.object_schemas import ObjectReturn
from app.api.schemas.object_schemas import ObjectUpdateParameters
from app.utils.unitofwork import IUnitOfWork


class ObjectService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_one_object_by_id(self, id: int, user_id: int):
        async with self.uow:
            object = await self.uow.objects.find_by_main_object_id(id)
            if object:
                if object.user_id == user_id or object.status == "public":
                    return ObjectReturn.model_validate(object)
                else:
                    raise HTTPException(403, "Пользователь не является владельцем объекта")
            else:
                raise HTTPException(400, "Такого объекта не существует")

    async def get_versions_by_id(self, id: int, user_id: int):
        async with self.uow:
            objects = await self.uow.objects.find_all_by_main_object_id(id)
            if objects:
                if objects[0].user_id == user_id:
                    return [AllObjectReturn.model_validate(i) for i in objects]
                else:
                    raise HTTPException(403, "Пользователь не является владельцем объекта")
            else:
                raise HTTPException(400, "Такого объекта не существует")

    """async def get_public_object_by_id(self, id: int):
        async with self.uow:
            object = await self.uow.objects.find_by_id_public(id)
            if not object:
                raise HTTPException(404, "Публичных объектов с этим id не существует")
            object = ObjectReturn.model_validate(object)
            return object"""

    async def create_object(self, user_id: int, title: str):
        async with self.uow:
            object_id = await self.uow.objects.add_object(user_id=user_id, title=title)
            await self.uow.commit()
            return object_id

    async def update(self, object: ObjectUpdateParameters, user_id: int):
        async with self.uow:
            db_object = await self.uow.objects.find_by_main_object_id(object.main_object_id)
            if not db_object:
                raise HTTPException(400, "Такого объекта не существует")
            if object.user_id == user_id:
                """if object.status == "check":
                    raise HTTPException(400, "объект находится на проверке")"""
                await self.uow.objects.update(title=object.title, file=object.file,
                                              id=object.main_object_id, user_id=object.user_id)
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем объекта")

    """async def get_all_public_objects(self):
        async with self.uow:
            objects = await self.uow.objects.find_all_public_objects()
            return [AllObjectReturn.model_validate(i) for i in objects]"""

    async def get_all_user_objects(self, user_id: int, user: int):
        async with self.uow:
            if user_id != user:
                raise HTTPException(403, "Пользователь не является владельцем объектов")
            objects = await self.uow.objects.find_all_user_objects(user_id)
            return [ObjectReturn.model_validate(i) for i in objects]

    """async def get_all_user_public_objects(self, user_id: int):
        async with self.uow:
            objects = await self.uow.objects.find_all_user_public_objects(user_id)
            return [ObjectReturn.model_validate(i) for i in objects]"""

    async def publication_request(self, object_id: int, user_id: int):
        async with self.uow:
            db_object = await self.uow.objects.find_by_id_private(object_id)
            if not db_object:
                raise HTTPException(400, "Такого объекта не существует")
            if db_object.user_id == user_id:
                if db_object.status == "public":
                    raise HTTPException(400, "объект уже опубликован")
                await self.uow.objects.change_status(object_id, "public")
                await self.uow.commit()
            else:
                raise HTTPException(403, "Пользователь не является владельцем объекта")

    async def delete_object(self, object_id: int, user_id: int):
        async with self.uow:
            db_object = await self.uow.objects.find_all_by_main_object_id(object_id)
            if not db_object:
                raise HTTPException(400, "Такого объекта не существует")
            if db_object[0].user_id != user_id:
                raise HTTPException(403, "Пользователь не является владельцем объекта")
            for object in db_object:
                await self.uow.objects.del_one(id=object.id)
            await self.uow.commit()

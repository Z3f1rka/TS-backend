from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

# from app.api.schemas import AllObjectReturn
from app.api.schemas import ObjectCreateParameters
from app.api.schemas import ObjectReturn
from app.api.schemas import ObjectUpdateParameters
from app.services import ObjectService
from app.utils import get_jwt_payload
from app.utils import IUnitOfWork
from app.utils import UnitOfWork

router = APIRouter(tags=["Working with objects"], prefix="/objects")


async def get_object_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> ObjectService:  # noqa
    return ObjectService(uow)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(jwt_access: Annotated[str, Depends(get_jwt_payload)], object: ObjectCreateParameters,
                 service: ObjectService = Depends(get_object_service)) -> int:  # noqa
    """Создание объекта"""
    return await service.create_object(int(jwt_access["sub"]), object.title)


@router.post("/update", status_code=status.HTTP_200_OK)
async def update(jwt_access: Annotated[str, Depends(get_jwt_payload)], object: ObjectUpdateParameters,
                 service: ObjectService = Depends(get_object_service)):  # noqa
    """Изменение объекта"""
    await service.update(object, int(jwt_access["sub"]))


"""@router.get("/get_by_id_private")
async def get_private(object_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)],
                      service: ObjectService = Depends(get_object_service)) -> ObjectReturn:  # noqa
    object = await service.get_private_object_by_id(object_id, user_id=int(jwt_access["sub"]))
    return object


@router.get("/get_by_id_public")
async def get_public(object_id: int, service: ObjectService = Depends(get_object_service)) -> ObjectReturn:  # noqa
    object = await service.get_public_object_by_id(object_id)
    return object


@router.get('/all_public_objects')
async def get_all_objects(service: ObjectService = Depends(get_object_service)) -> list[AllObjectReturn]:  # noqa
    objects = await service.get_all_public_objects()
    return objects"""


@router.get('/all_user_objects')
async def get_all_user_objects(user_id: int, jwt_access: Annotated[str, Depends(get_jwt_payload)],
                              service: ObjectService = Depends(get_object_service)) -> list[ # noqa
    ObjectReturn]:  # noqa
    """Получение всех приватных и публичных объектов пользователя. Для запроса нужен токен."""
    objects = await service.get_all_user_objects(user_id=user_id, user=int(jwt_access["sub"]))
    return objects


"""@router.get('/all_user_public_objects')
async def get_all_user_public_objects(user_id: int, service: ObjectService = Depends(get_object_service)) -> list[ # noqa
    ObjectReturn]:  # noqa
    objects = await service.get_all_user_public_objects(user_id)
    return objects"""


@router.delete('/delete_object')
async def delete_object(jwt_access: Annotated[str, Depends(get_jwt_payload)], object_id: Annotated[int, Query()], # noqa
                       service: ObjectService = Depends(get_object_service)): # noqa
    """Удаление объекта"""
    await service.delete_object(object_id=object_id, user_id=int(jwt_access["sub"]))

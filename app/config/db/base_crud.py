from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    @classmethod
    async def create(cls, db: AsyncSession, **obj_attrs):
        obj = cls(**obj_attrs)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def update(cls, db: AsyncSession, pk: int, obj_attrs: dict):
        obj = await cls.get(db, pk)
        for attr, value in obj_attrs.items():
            setattr(obj, attr, value)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def get(cls, db: AsyncSession, pk: int):
        return await db.get(cls, pk)

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def delete(cls, db: AsyncSession, pk: int):
        obj = await cls.get(db, pk)
        await db.delete(obj)
        await db.commit()
        return obj

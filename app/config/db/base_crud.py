from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
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

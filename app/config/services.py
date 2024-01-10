from fastapi import HTTPException
from starlette import status


async def get_object_or_404(db, model, pk):
    obj = await model.get(db, pk)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model} with id {pk} not found")
    return obj

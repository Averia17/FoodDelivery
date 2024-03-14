from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative, declared_attr


def to_underscore(name):
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return to_underscore(cls.__name__)

    def __repr__(self):
        return f"{self.__tablename__}: {self.id}"

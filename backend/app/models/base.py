import uuid
from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    update_at = Column(
        DateTime, server_default=func.now(), nullable=False
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

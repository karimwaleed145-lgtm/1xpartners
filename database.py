from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DB_URL


class Base(DeclarativeBase):
    pass


class Partner(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    language: Mapped[str] = mapped_column(String(4), default="en")
    full_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128))
    promocode: Mapped[str] = mapped_column(String(64))
    phone: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


engine = create_async_engine(DB_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_partner(**kwargs) -> int:
    async with Session() as s:
        p = Partner(**kwargs)
        s.add(p)
        await s.commit()
        return p.id

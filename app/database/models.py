from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

#Запуск создания БД
async_session = async_sessionmaker(engine, class_=AsyncSession)

#       через этот класс происходит управление всеми моделями
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)


class Manicurist(Base):
    __tablename__ = 'manicurists'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))


class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))


class Day(Base):
    __tablename__ = 'days'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))

class Hour(Base):
    __tablename__ = 'hours'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[int]


class Reserve(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    manicurist: Mapped[int] = mapped_column(ForeignKey('manicurists.id'))
    service: Mapped[int] = mapped_column(ForeignKey('services.id'))
    day: Mapped[int] = mapped_column(ForeignKey('days.id'))
    hour: Mapped[int] = mapped_column(ForeignKey('hours.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

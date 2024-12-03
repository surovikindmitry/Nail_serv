from sqlalchemy import ForeignKey, String, BigInteger, select, join
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)


class Barber(Base):
    __tablename__ = 'barbers'

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
    name: Mapped[str] = mapped_column(String(20))


class Reserve(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    barber: Mapped[int] = mapped_column(ForeignKey('barbers.id'))
    service: Mapped[int] = mapped_column(ForeignKey('services.id'))
    day: Mapped[int] = mapped_column(ForeignKey('days.id'))
    hour: Mapped[int] = mapped_column(ForeignKey('hours.id'))



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



stmt = (
    select(
        User.name.label("username"),
        User.phone_number.label("phone_number"),
        Barber.name.label("barber_name"),
        Service.name.label("service_name"),
        Day.name.label("day_name"),
        Hour.name.label("hour_name")
    )
    .select_from(join(
        Reserve,
        User, Reserve.user == User.id
    ))
    .join(Barber, Reserve.barber == Barber.id)
    .join(Service, Reserve.service == Service.id)
    .join(Day, Reserve.day == Day.id)
    .join(Hour, Reserve.hour == Hour.id)
)

async def get_data():
    async with async_session() as session:
        result = await session.execute(stmt)

        data_to_send = []
        for row in result.all():
            data_to_send.append((
                row.username,
                row.phone_number,
                row.barber_name,
                row.service_name,
                row.day_name,
                row.hour_name,

            ))
    return data_to_send
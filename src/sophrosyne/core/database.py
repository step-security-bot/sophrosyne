"""This module is responsible for creating the database and tables, and also for creating the root user."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sophrosyne.core.config import get_settings
from sophrosyne.core.logging import get_logger
from sophrosyne.core.models import Profile, User
from sophrosyne.core.security import new_token, sign

engine = create_async_engine(
    get_settings().database.dsn,
    echo=get_settings().development.sqlalchemy_echo,
    future=True,
)

log = get_logger()


async def create_db_and_tables():
    """Create the database and tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_default_profile():
    """Create the default profile if it does not exist."""
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        result = await session.exec(
            select(Profile).where(Profile.name == get_settings().default_profile)
        )
        p = result.first()
        if p:
            return ""

        profile = Profile(name=get_settings().default_profile)
        session.add(profile)
        await session.commit()

        return profile


async def create_root_user() -> str:
    """Create the root user if it does not exist."""
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        result = await session.exec(
            select(User).where(User.contact == get_settings().root_contact)
        )
        u = result.first()
        if u:
            return ""

        token = new_token()
        if get_settings().development.static_root_token != "":
            token = get_settings().development.static_root_token
            log.warn("static root token in use")
        user = User(
            name="root",
            contact=get_settings().root_contact,
            signed_token=sign(token),
            is_active=True,
            is_admin=True,
        )
        session.add(user)
        await session.commit()

        return token

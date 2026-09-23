from __future__ import annotations

from pathlib import Path

from sqlalchemy import Boolean, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .config import DATABASE_URL

if DATABASE_URL.startswith("sqlite") and "///" in DATABASE_URL:
    db_path = DATABASE_URL.split("///", 1)[1]
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), index=True)
    username: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def list_categories(session: AsyncSession) -> list[str]:
    rows = (
        await session.execute(
            select(Channel.category).distinct().order_by(Channel.category)
        )
    ).scalars().all()
    return list(rows)


async def get_channels(
    session: AsyncSession,
    category: str | None = None,
    featured: bool | None = None,
) -> list[Channel]:
    stmt = select(Channel).order_by(Channel.name)
    if category:
        stmt = stmt.where(Channel.category == category)
    if featured is not None:
        stmt = stmt.where(Channel.featured == featured)
    return list((await session.execute(stmt.limit(50))).scalars().all())


async def search_channels(session: AsyncSession, query: str) -> list[Channel]:
    pattern = f"%{query.lower()}%"
    stmt = (
        select(Channel)
        .where(
            Channel.name.ilike(pattern)
            | Channel.description.ilike(pattern)
            | Channel.category.ilike(pattern)
        )
        .order_by(Channel.featured.desc(), Channel.name)
        .limit(20)
    )
    return list((await session.execute(stmt)).scalars().all())


async def seed_demo_data() -> None:
    async with SessionLocal() as session:
        existing = (await session.execute(select(Channel.id).limit(1))).first()
        if existing:
            return

        session.add_all(
            [
                Channel(
                    name="Technology Updates",
                    description="General technology news, tools, and learning resources.",
                    category="Technology",
                    featured=True,
                ),
                Channel(
                    name="Education Hub",
                    description="Study resources, learning tips, and educational content.",
                    category="Education",
                    featured=True,
                ),
                Channel(
                    name="Business Daily",
                    description="Business ideas, entrepreneurship, and practical business information.",
                    category="Business",
                    featured=False,
                ),
            ]
        )
        await session.commit()

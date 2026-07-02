from typing import Optional
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.db.models import Post, Rubric
from src.elastic.search import elasticsearcher
from pydantic import BaseModel, ConfigDict


class ElasticsearchDoc(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)


async def create_post(session: AsyncSession, text: str) -> Post:
    post = Post(text=text)
    session.add(post)
    await session.commit()
    await session.refresh(post)

    doc = ElasticsearchDoc.model_validate(post).model_dump()
    await elasticsearcher.add_doc(doc)

    return post


async def get_post(session: AsyncSession, post_id: int | str) -> Post | None:
    post_id = int(post_id)
    stmt = select(Post).where(Post.id == post_id)
    result: Result = await session.execute(stmt)
    post: Optional[Post] = result.scalar_one_or_none()
    return post


async def get_posts_by_ids(
    session: AsyncSession, posts_ids: list[str | int]
) -> list[Post]:
    posts_ids = [int(i) for i in posts_ids]
    stmt = select(Post).where(Post.id.in_(posts_ids)).order_by(Post.created_date.desc())
    result: Result = await session.execute(stmt)
    posts = result.all()
    return posts


async def get_all_posts(session: AsyncSession) -> list[Optional[Post]]:
    stmt = select(Post)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def update_post(session: AsyncSession, post: Post, new_text: str) -> Post:
    post.text = new_text
    await session.commit()
    await session.refresh(post)
    return post


async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()

    doc = await elasticsearcher.search_db_id(post.id)
    id = await elasticsearcher.get_docs_ids_from_search(doc)
    id = id[0]
    await elasticsearcher.delete_doc(id)


async def add_rubric_to_post(session: AsyncSession, post: Post, vk_id: str) -> Rubric:
    rubric = Rubric(post_id=post.id, vk_id=vk_id)
    session.add(rubric)
    await session.commit()
    await session.refresh(rubric)
    return rubric


async def get_rubrics_for_post(session: AsyncSession, post: Post) -> list[Rubric]:
    stmt = select(Rubric).where(Rubric.post_id == post.id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def get_rubrics_ids_for_post(session: AsyncSession, post: Post) -> list[str]:
    rubrics = await get_rubrics_for_post(session, post)
    return [i.vk_id for i in rubrics]


async def create_rubric(
    session: AsyncSession, post_id: int | str, vk_id: str
) -> Rubric:
    post_id = int(post_id)
    rubric = Rubric(post_id=post_id, vk_id=vk_id)
    session.add(rubric)
    await session.commit()
    await session.refresh(rubric)
    return rubric


async def get_rubric(session: AsyncSession, rubric_id: int | str) -> Rubric | None:
    stmt = select(Rubric).where(Rubric.id == int(rubric_id))
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_rubrics(session: AsyncSession) -> list[Rubric]:
    stmt = select(Rubric)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


async def update_rubric(
    session: AsyncSession, rubric: Rubric, new_vk_id: str
) -> Rubric:
    rubric.vk_id = new_vk_id
    await session.commit()
    await session.refresh(rubric)
    return rubric


async def delete_rubric(session: AsyncSession, rubric: Rubric) -> None:
    await session.delete(rubric)
    await session.commit()

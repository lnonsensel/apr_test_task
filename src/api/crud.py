from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from src.db import crud as db_crud
from src.api.schemas import (
    PostCreate,
    Post,
    PostUpdate,
    Rubric,
    RubricCreate,
    RubricUpdate,
)

crud_router = APIRouter(prefix="/crud")

post_router = APIRouter(prefix="/post", tags=["Posts"])
rubric_router = APIRouter(prefix="/rubric", tags=["Rubrics"])

crud_router.include_router(post_router)
crud_router.include_router(rubric_router)


@post_router.post(
    "/",
    response_model=Post,
    status_code=201,
    summary="Create new post",
    description="Creates new post in the database",
    response_description="Successfully created post JSON object",
)
async def create_post(
    request_model: PostCreate, db: AsyncSession = Depends(get_session)
):
    new_post = await db_crud.create_post(db, request_model.text)

    for rubric in request_model.rubrics:
        await db_crud.add_rubric_to_post(db, new_post, rubric)

    rubrics = await db_crud.get_rubrics_ids_for_post(db, new_post)
    post_model = Post.model_validate_with_rubrics(new_post, rubrics)
    return post_model


@post_router.post(
    "/{post_id}",
    response_model=Post,
    status_code=200,
    summary="Updates existing post",
    description="Updates post entry in the database",
    response_description="Successfully updated post JSON object",
    responses={404: {"description": "Post not found"}},
)
async def update_post(
    post_id: str, request_model: PostUpdate, db: AsyncSession = Depends(get_session)
):
    if request_model.text is not None:
        post = await db_crud.get_post(db, post_id)
        if post is None:
            raise HTTPException(404, "Post not found")
        await db_crud.update_post(db, post, request_model.text)
        rubrics = await db_crud.get_rubrics_ids_for_post(db, post)
        return Post.model_validate_with_rubrics(post, rubrics)


@post_router.get(
    "/{post_id}",
    response_model=Post,
    status_code=200,
    summary="Gets existing post",
    description="Gets post entry in the database",
    response_description="Successfully extracted post JSON object",
    responses={404: {"description": "Post not found"}},
)
async def read_post(post_id: str | int, db: AsyncSession = Depends(get_session)):
    post_id = int(post_id)
    post = await db_crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(404, "Post not found")
    rubrics = await db_crud.get_rubrics_ids_for_post(db, post)
    post_model = Post.model_validate_with_rubrics(post, rubrics)
    return post_model


@post_router.delete(
    "/{post_id}",
    status_code=200,
    summary="Deletes existing post",
    description="Deletes post entry in the database",
    response_description="none",
    responses={404: {"description": "Post not found"}},
)
async def delete_post(post_id: str | int, db: AsyncSession = Depends(get_session)):
    post_id = int(post_id)
    post = await db_crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(404, "Post not found")
    await db_crud.delete_post(db, post)


@rubric_router.post(
    "/",
    response_model=Rubric,
    status_code=201,
    summary="Creates new rubric",
    description="Creates new rubric in the database",
    response_description="Successfully created rubric JSON object",
)
async def create_rubric(
    request_model: RubricCreate, db: AsyncSession = Depends(get_session)
):
    new_post = await db_crud.create_rubric(
        db, request_model.post_id, request_model.vk_id
    )
    return Rubric.model_validate(new_post)


@rubric_router.post(
    "/{rubric_id}",
    response_model=Rubric,
    status_code=200,
    summary="Updates existing rubric",
    description="Updates existing rubric in the database",
    response_description="Successfully updated rubric JSON object",
    responses={404: {"description": "Rubric not found"}},
)
async def update_rubric(
    rubric_id: str, request_model: RubricUpdate, db: AsyncSession = Depends(get_session)
):
    if request_model.vk_id is not None:
        rubric = await db_crud.get_rubric(db, rubric_id)
        if rubric is None:
            raise HTTPException(404, "Rubric not found")
        await db_crud.update_rubric(db, rubric, request_model.vk_id)
        return Rubric.model_validate(rubric)


@rubric_router.get(
    "/{rubric_id}",
    response_model=Rubric,
    status_code=200,
    summary="Gets existing rubric",
    description="Gets existing rubric in the database",
    response_description="Successfully extracted rubric JSON object",
    responses={404: {"description": "Rubric not found"}},
)
async def read_rubric(rubric_id: str | int, db: AsyncSession = Depends(get_session)):
    post = await db_crud.get_rubric(db, rubric_id)
    if post is None:
        raise HTTPException(404, "Rubric not found")
    return Rubric.model_validate(post)


@rubric_router.delete(
    "/{rubric_id}",
    status_code=200,
    summary="Deletes existing rubric",
    description="Deletes existing rubric in the database",
    response_description="none",
    responses={404: {"description": "Rubric not found"}},
)
async def delete_rubric(rubric_id: str, db: AsyncSession = Depends(get_session)):
    rubric = await db_crud.get_rubric(db, rubric_id)
    if rubric is None:
        raise HTTPException(404, "Rubric not found")
    await db_crud.delete_post(db, rubric)

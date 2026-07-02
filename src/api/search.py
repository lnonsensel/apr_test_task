from elastic_transport import ObjectApiResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from src.db import crud as db_crud
from src.api.schemas import Post, SearchRequest, SearchResponse
from src.elastic.search import elasticsearcher


search_router = APIRouter(prefix="/search", tags=["Search"])


@search_router.post(
    "/",
    response_model=SearchResponse,
    status_code=201,
    summary="Search by text among post texts",
    description="Searches by text among post texts using elasticsearch",
    response_description="search_size posts from database that elasticsearch returned for sent text query",
    tags=["Search"],
)
async def search_text_in_post(
    request_model: SearchRequest, db: AsyncSession = Depends(get_session)
):
    search_result = await elasticsearcher.search_text(request_model.text)
    ids = await elasticsearcher.get_ids_from_search(search_result)
    posts = await db_crud.get_posts_by_ids(db, ids)
    posts_models = []
    for post in posts:
        post = post[0]
        rubrics = await db_crud.get_rubrics_ids_for_post(db, post)
        posts_models.append(Post.model_validate_with_rubrics(post, rubrics))
    return SearchResponse(posts=posts_models)

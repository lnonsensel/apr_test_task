from typing import Optional
from src.elastic import config
from src.elastic.index_mgr import ElasticIndexManager


class Elasticsearcher(ElasticIndexManager):
    def __init__(
        self, index: Optional[str] = None, search_size: Optional[int] = None
    ) -> None:
        super().__init__(index)
        if search_size is None:
            self.search_size = config.search_size
        else:
            self.search_size = search_size

    async def search(self, match_key: str, match_val: str | int) -> dict:
        response = await self.client.search(
            index=self.index,
            query={"match": {match_key: match_val}},
            size=self.search_size,
        )
        return dict(response)

    async def search_term(self, term_key: str, term_val: str | int) -> dict:
        response = await self.client.search(
            index=self.index,
            query={"term": {term_key: term_val}},
        )
        return dict(response)

    async def get_ids_from_search(self, search_result: dict):
        return [i["_source"]["id"] for i in search_result["hits"]["hits"]]

    async def get_docs_ids_from_search(self, search_result: dict):
        return [i["_id"] for i in search_result["hits"]["hits"]]

    async def search_text(self, text: str):
        response = await self.search("text", text)
        return response

    async def search_db_id(self, db_id: int):
        response = await self.search_term("id", db_id)
        return response


elasticsearcher = Elasticsearcher()

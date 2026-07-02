from typing import Any, Optional
import os
from src.elastic.connector import ElasticConnector
from src.elastic import config


class ElasticIndexManager(ElasticConnector):
    def __init__(self, index: Optional[str] = None) -> None:
        super().__init__()
        if index is None:
            self.index = os.getenv("ELASTIC_INDEX")
        else:
            self.index = index

        if self.index is None:
            raise Exception("No index provided")

    async def create_index(self, mappings: Optional[dict[str, Any]] = None):
        if mappings is None:
            mappings = config.mappings
        if not await self.client.indices.exists(index=self.index):
            await self.client.indices.create(index=self.index, mappings=mappings)

    async def add_doc(self, document: dict, id: Optional[str] = None):
        await self.client.index(index=self.index, document=document, id=id)

    async def delete_doc(self, id: str):
        await self.client.delete(index=self.index, id=id)

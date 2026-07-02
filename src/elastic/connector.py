from json import load
import os
from elasticsearch import AsyncElasticsearch
from dotenv import load_dotenv


class ElasticConnector:
    def __init__(self) -> None:
        load_dotenv(".elastic.env")
        url = os.getenv("ELASTIC_URL")
        user = os.getenv("ELASTIC_USER")
        password = os.getenv("ELASTIC_PASSWORD")
        auth = None
        if user is not None and password is not None:
            auth = (user, password)

        self.client = AsyncElasticsearch(url, basic_auth=auth)

    def check_connection(
        self,
    ):
        pass

import asyncio
import aiohttp
import pandas as pd
from asyncio import Semaphore
import json


def read_file(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def parse_all_rows(df: pd.DataFrame) -> list:
    df["rubrics"] = df["rubrics"].apply(str.replace, args=("'", '"'))
    df["rubrics"] = df["rubrics"].apply(json.loads)
    return df.to_dict("records")


async def create_posts_async(url: str, data_list: list, max_concurrent: int = 20):
    semaphore = Semaphore(max_concurrent)

    async def post_one(session, data):
        async with semaphore:
            async with session.post(url, json=data) as response:
                response.raise_for_status()
                return await response.text()

    async with aiohttp.ClientSession() as session:
        tasks = [post_one(session, data) for data in data_list]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    sample_data_file = "posts.csv"
    fastapi_url = "http://0.0.0.0:3000/crud/post"

    df = read_file(sample_data_file)
    parsed_objs = parse_all_rows(df)

    asyncio.run(create_posts_async(fastapi_url, parsed_objs, max_concurrent=20))

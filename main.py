import asyncio

import httpx
import pydantic
from pydantic import BaseModel

BASE_URL = "https://jsonplaceholder.typicode.com/"

class Post(BaseModel):
    userId: int
    title: str
    body: str

async def fetch_data(post_id:int):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=BASE_URL + f"posts/{post_id}")
        response.raise_for_status()
        Post.model_validate(response.json())
        print(response.json())

async def main():
    print("Fetching data...")
    await asyncio.gather(*(fetch_data(i) for i in range(1,4)))
    print("All data fetched concurrently")


if __name__ == "__main__":
    asyncio.run(main())

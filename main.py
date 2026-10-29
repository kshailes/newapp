import asyncio

import httpx
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

from app.config import get_settings




async def fetch_data(post_id:int, base_url:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=base_url + f"posts/{post_id}")
        print(response.json())

async def main():
    settings = get_settings()
    print("Fetching data...")
    await asyncio.gather(*(fetch_data(i,settings.BASE_URL) for i in range(1,4)))
    print("All data fetched concurrently")


if __name__ == "__main__":
    asyncio.run(main())

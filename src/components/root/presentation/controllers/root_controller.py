from typing import Awaitable, Optional, Dict

import aiohttp

from fastapi import APIRouter

router = APIRouter()


async def get_root_through_network() -> Awaitable[Optional[Dict]]:
    rst = None
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/") as resp:
            try:
                rst = await resp.json()
            except Exception as exc:
                import traceback

                print("#Poor_Logging_For_Only_Sample_Purpose:", exc)
                traceback.print_exc()
                print("#End_Of_Poor_Logging")

    return rst


@router.get("/")
async def root():
    return {"message": "Server is running."}


@router.get("/foo")
async def foo():
    root_data = await get_root_through_network()

    if type(root_data) is dict:
        root_data["foo_additional"] = "foo"

    return root_data

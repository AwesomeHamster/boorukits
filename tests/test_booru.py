import asyncio
import os

from tests.utils import expect_image, expect_image_list
from typing import List

import pytest

from boorukits import BooruFactory

PROXY = os.environ.get("HTTP_PROXY", None)

sites: List[str] = [
    "Danbooru",
    "Gelbooru",
    "Konachan",
    "KonachanR18",
    "Safebooru"
]


@pytest.mark.asyncio
async def test_all():
    await asyncio.gather(*(list(map(lambda name: get_posts(name), sites))))


async def get_posts(name: str):
    booru = BooruFactory.get(name, proxy=PROXY)
    if booru:
        response = await booru.get_posts()

        expect_image_list(response)
        img_id = response[0].id
        img = await booru.get_post(img_id)
        
        expect_image(img)

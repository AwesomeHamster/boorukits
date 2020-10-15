import os
from tests.utils import expect_image, expect_image_list
from typing import List

import pytest

from boorukits import Gelbooru, GelbooruImage

PROXY = os.environ.get("HTTP_PROXY", None)


@pytest.mark.asyncio
async def test_get_posts():
    gelbooru = Gelbooru(proxy=PROXY)
    response: List[GelbooruImage] = await gelbooru.get_posts("*")

    expect_image_list(response)


@pytest.mark.asyncio
async def test_get_post():
    gelbooru = Gelbooru(proxy=PROXY)
    # kokkoro from princess connect!
    # https://gelbooru.com/index.php?page=post&s=view&id=5552990&tags=kokkoro_%28princess_connect%21%29
    img: GelbooruImage = await gelbooru.get_post("5552990")

    expect_image(img)

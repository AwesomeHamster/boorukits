import os
from typing import List

import pytest
from boorukits import Konachan, KonachanImage

from tests.utils import expect_image, expect_image_list

PROXY = os.environ.get("HTTP_PROXY", None)


@pytest.mark.asyncio
async def test_get_posts():
    konachan = Konachan(proxy=PROXY)
    response: List[KonachanImage] = await konachan.get_posts("*")

    expect_image_list(response)


@pytest.mark.asyncio
async def test_get_post():
    konachan = Konachan(proxy=PROXY)
    # kokkoro from princess connect!
    # https://konachan.com/post/show/314675/blush-gray_hair-kokkoro-navel-pointed_ears-princes
    img: List[KonachanImage] = await konachan.get_post("314675")

    expect_image(img)

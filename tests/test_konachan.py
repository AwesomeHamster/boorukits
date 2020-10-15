import asyncio
import os
from typing import List

import pytest
from boorukits import Konachan, KonachanImage, KonachanR18

from tests.utils import expect_image, expect_image_list

PROXY = os.environ.get("HTTP_PROXY", None)


@pytest.mark.asyncio
async def test_get_posts():
    konachan = Konachan(proxy=PROXY)
    konachanR18 = KonachanR18(proxy=PROXY)
    responses: List[List[KonachanImage]] = await asyncio.gather(
        konachan.get_posts("*"), konachanR18.get_posts("*"))

    for response in responses:
        expect_image_list(response)


@pytest.mark.asyncio
async def test_get_post():
    konachan = Konachan(proxy=PROXY)
    konachanR18 = KonachanR18(proxy=PROXY)
    # kokkoro from princess connect!
    # https://konachan.com/post/show/314675/blush-gray_hair-kokkoro-navel-pointed_ears-princes
    responses: List[KonachanImage] = await asyncio.gather(
        konachan.get_post("314675"), konachanR18.get_post("314675"))

    for img in responses:
        expect_image(img)

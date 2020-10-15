from tests.utils import expect_image, expect_image_list
from typing import List

import pytest

from boorukits import Safebooru, SafebooruImage


@pytest.mark.asyncio
async def test_get_posts():
    safebooru = Safebooru()
    response: List[SafebooruImage] = await safebooru.get_posts("*")

    expect_image_list(response)


@pytest.mark.asyncio
async def test_get_post():
    safebooru = Safebooru()
    # kokkoro from princess connect!
    # https://safebooru.org/index.php?page=post&s=view&id=3227726
    img: List[SafebooruImage] = await safebooru.get_post("3227726")

    expect_image(img)

from typing import List

import pytest

from boorukits import Gelbooru, GelbooruImage


@pytest.mark.asyncio
async def test_get_posts():
    gelbooru = Gelbooru()
    response: List[GelbooruImage] = await gelbooru.get_posts("*")

    assert isinstance(response, list)
    assert len(response) > 0
    assert isinstance(response[0], GelbooruImage)

    img: GelbooruImage = response[0]
    assert img.tags
    assert isinstance(img.tags_list, list)
    assert len(img.tags_list) >= 1
    assert img.file_url


@pytest.mark.asyncio
async def test_get_post():
    gelbooru = Gelbooru()
    # kokkoro from princess connect!
    # https://gelbooru.com/index.php?page=post&s=view&id=5552990&tags=kokkoro_%28princess_connect%21%29
    img: List[GelbooruImage] = await gelbooru.get_post("5552990")

    assert isinstance(img, GelbooruImage)

    assert img.tags
    assert isinstance(img.tags_list, list)
    assert len(img.tags_list) >= 1
    assert img.file_url

from typing import List

import pytest

from boorukits import Safebooru, SafebooruImage


@pytest.mark.asyncio
async def test_get_posts():
    safebooru = Safebooru()
    response: List[SafebooruImage] = await safebooru.get_posts("*")

    assert isinstance(response, list)
    assert len(response) > 0
    assert isinstance(response[0], SafebooruImage)

    img: SafebooruImage = response[0]
    assert img.tags
    assert isinstance(img.tags_list, list)
    assert len(img.tags_list) >= 1
    assert img.file_url


@pytest.mark.asyncio
async def test_get_post():
    safebooru = Safebooru()
    # kokkoro from princess connect!
    # https://safebooru.org/index.php?page=post&s=view&id=3227726
    img: List[SafebooruImage] = await safebooru.get_post("3227726")

    assert isinstance(img, SafebooruImage)

    assert img.tags
    assert isinstance(img.tags_list, list)
    assert len(img.tags_list) >= 1
    assert img.file_url

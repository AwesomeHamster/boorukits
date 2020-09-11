from typing import List

import pytest

from boorukits import Danbooru, DanbooruImage


@pytest.mark.asyncio
async def test_get_posts():
    danbooru = Danbooru(api_url="https://testbooru.donmai.us")
    response: List[DanbooruImage] = await danbooru.get_posts("*")
    assert(isinstance(response, list))
    assert(len(response) > 0)
    assert(isinstance(response[0], DanbooruImage))
    assert(response[0].file_url)


@pytest.mark.asyncio
async def test_posts():
    danbooru = Danbooru()
    response: List[DanbooruImage] = await danbooru.get_posts("yazawa_nico")
    assert(isinstance(response, list))
    img = response[0]
    assert(isinstance(img.tags_list, list))
    assert(len(img.tags_list) >= 1)

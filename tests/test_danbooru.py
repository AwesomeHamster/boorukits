from typing import List
import os
import asyncio

import pytest

from boorukits import Danbooru, DanbooruImage


def get_ragular_site():
    return Danbooru()


def get_test_site():
    return Danbooru(api_url="https://testbooru.donmai.us")


def get_ragular_site_with_api_key():
    user = os.environ.get("DANBOORU_USER", None)
    token = os.environ.get("DANBOORU_TOKEN", None)
    assert user and token
    return Danbooru(username=user, api_key=token)


@pytest.mark.asyncio
async def test_get_posts():
    danboorus: List[Danbooru] = [get_ragular_site(), get_test_site(), get_ragular_site_with_api_key()]
    get_posts = list(map(lambda danbooru: danbooru.get_posts("*"), danboorus))
    done: List[List[DanbooruImage]] = asyncio.gather(get_posts)

    for response in done:
        assert isinstance(response, list)
        assert len(response) > 0
        assert isinstance(response[0], DanbooruImage)
        assert response[0].file_url


@pytest.mark.asyncio
async def test_posts():
    danboorus: List[Danbooru] = [get_ragular_site(), get_ragular_site_with_api_key()]
    get_posts = list(map(lambda danbooru: danbooru.get_posts("yazawa_nico"), danboorus))
    done: List[List[DanbooruImage]] = asyncio.gather(get_posts)

    for response in done:
        assert isinstance(response, list)
        img = response[0]
        assert isinstance(img.tags_list, list)
        assert len(img.tags_list) >= 1

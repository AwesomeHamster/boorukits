import asyncio
import os
from typing import List

import pytest

from boorukits import Danbooru, DanbooruImage


def get_ragular_site():
    return Danbooru()


def get_test_site():
    return Danbooru(root_url="https://testbooru.donmai.us")


def get_ragular_site_with_token():
    user = os.environ.get("DANBOORU_USER", None)
    token = os.environ.get("DANBOORU_TOKEN", None)
    # assume token is passed
    assert user and token
    return Danbooru(user=user, token=token)


@pytest.mark.asyncio
async def test_get_posts():
    danboorus: List[Danbooru] = [
        get_ragular_site(),
        get_test_site(),
        get_ragular_site_with_token(),
    ]
    get_posts = list(map(lambda danbooru: danbooru.get_posts("*"), danboorus))
    done: List[List[DanbooruImage]] = await asyncio.gather(*get_posts)

    for response in done:
        assert isinstance(response, list)
        assert len(response) > 0
        assert isinstance(response[0], DanbooruImage)

        img: DanbooruImage = response[0]
        assert img.tags
        assert isinstance(img.tags_list, list)
        assert len(img.tags_list) >= 1
        assert img.file_url


@pytest.mark.asyncio
async def test_posts_with_tags():
    danboorus: List[Danbooru] = [
        get_ragular_site(), get_ragular_site_with_token()
    ]
    get_posts = list(
        map(lambda danbooru: danbooru.get_posts("yazawa_nico"), danboorus))
    done: List[List[DanbooruImage]] = await asyncio.gather(*get_posts)

    for response in done:
        assert isinstance(response, list)
        img = response[0]
        assert isinstance(img.tags_list, list)
        assert len(img.tags_list) >= 1


@pytest.mark.asyncio
async def test_post_by_id():
    danboorus: List[Danbooru] = [
        get_ragular_site(), get_ragular_site_with_token()
    ]
    # https://danbooru.donmai.us/posts/3134895
    # kokkoro from pricess connect!
    get_post = list(
        map(lambda danbooru: danbooru.get_post("3134895"), danboorus))
    done: List[DanbooruImage] = await asyncio.gather(*get_post)

    for response in done:
        assert isinstance(response, DanbooruImage)
        assert response.id == "3134895"
        assert response.file_url
        assert response.sample_url
        assert response.thumbnail_url

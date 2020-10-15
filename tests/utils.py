from typing import List
from boorukits.booru import BooruImage


def expect_image(img: BooruImage):
    assert img.id
    assert img.tags
    assert isinstance(img.tags_list, list)
    assert len(img.tags_list) >= 1
    assert img.file_url


def expect_image_list(img_list: List[BooruImage]):
    assert isinstance(img_list, list)
    assert len(img_list) > 0
    for img in img_list:
        assert isinstance(img, BooruImage)
        expect_image(img)

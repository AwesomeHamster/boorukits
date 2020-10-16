from typing import Dict, Type

from .booru import Booru, BooruImage
from .errors import BooruError, InvalidResponseError
from .danbooru import Danbooru, DanbooruImage
from .gelbooru import Gelbooru, GelbooruImage
from .konachan import Konachan, KonachanImage, KonachanR18
from .safebooru import Safebooru, SafebooruImage

__all__ = [
    "Booru",
    "BooruImage",
    "Danbooru",
    "DanbooruImage",
    "Gelbooru",
    "GelbooruImage",
    "Safebooru",
    "SafebooruImage",
    "Konachan",
    "KonachanR18",
    "KonachanImage",
    "BooruError",
    "InvalidResponseError",
]

SITE_MAP: Dict[str, Type[Booru]] = {
    "danbooru": Danbooru,
    "gelbooru": Gelbooru,
    "konachan": Konachan,
    "konachan.net": Konachan,
    "konachan.com": KonachanR18,
    "konachanr18": KonachanR18,
    "safebooru": Safebooru,
}


class BooruFactory:

    @staticmethod
    def get(
        name: str = "",
        **kwargs,
    ):
        booru = SITE_MAP.get(name.lower(), None)
        if booru:
            return booru(**kwargs)
        return None

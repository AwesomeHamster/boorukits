from typing import List, Optional, Union

from boorukits.booru import BooruImage
from .gelbooru import Gelbooru

SAFEBOORU_API_URL = "https://safebooru.org/"


class SafebooruImage(BooruImage):

    @property
    def file_url(self):
        return SAFEBOORU_API_URL + \
            self._data_dict.get("directory", "") + \
            "/" + \
            self._data_dict.get("image", "")


class Safebooru(Gelbooru):
    """Wrap API of Safebooru (https://safebooru.org/)
    """

    def __init__(
        self,
        user: str = None,
        token: str = None,
        root_url: str = SAFEBOORU_API_URL,
        proxy: Optional[str] = None,
        loop=None,
    ) -> None:
        super().__init__(user=user,
            token=token,
            root_url=root_url,
            proxy=proxy,
            loop=loop)

    async def get_post(self, id: str = "") -> Union[SafebooruImage, None]:

        params = self._add_api_key({
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "id": id,
        })

        code, response = await self._get(self.root_url + "/index.php",
            params=params)

        # gelbooru would return a list even specify an id.
        res_image = response[0]
        return SafebooruImage(str(res_image.get("id", "-1")), res_image)

    async def get_posts(
        self,
        tags: str = "",
        page: int = None,
        limit: int = None,
        **kwargs,
    ) -> Union[List[SafebooruImage], None]:

        params = self._add_api_key({
            "page": "dapi",
            "s": "post",
            "q": "index",
            "tags": tags,
            "json": 1,
            "pid": page,
            "limit": limit,
        })

        code, response = await self._get(self.root_url + "/index.php",
            params=params,
            **kwargs)

        res_list = list()
        for i in response:
            # some post may lacks "id" property,
            # default to "-1".
            res_list.append(SafebooruImage(str(i.get("id", "-1")), i))
        return res_list

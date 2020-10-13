from typing import Any, Dict, List, Optional, Union

from .booru import Booru, BooruImage

API_URL = "https://gelbooru.com/"


class GelbooruImage(BooruImage):

    def __init__(self, iid: str, data_dict: Dict[str, Any]):
        super().__init__(iid, data_dict)

    @property
    def source(self) -> str:
        # there might be multiple source urls,
        # seperated by space
        sources = self._data_dict.get("source", "")
        return sources.split()[0]


class Gelbooru(Booru):
    """Wrap API of gelbooru (https://gelbooru.com/)

    See also: https://gelbooru.com/index.php?page=wiki&s=view&id=18780
    """

    def __init__(
        self,
        user: str = None,
        token: str = None,
        root_url: str = API_URL,
        proxy: Optional[str] = None,
        loop=None,
    ):
        super().__init__(proxy=proxy, loop=loop)
        self._user = user
        self._token = token
        self._root_url = root_url

    async def get_post(self, id: str = "") -> Union[GelbooruImage, None]:
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "id": id,
        }

        params = self._add_api_key(params)

        code, response = await self._get(self._root_url + "/index.php",
            params=params)

        # gelbooru would return a list even specify an id.
        res_image = response[0]
        return GelbooruImage(str(res_image.get("id", "-1")), res_image)

    async def get_posts(
        self,
        tags: str = "",
        page: int = None,
        limit: int = None,
        **kwargs,
    ) -> Union[List[GelbooruImage], None]:
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "tags": tags,
            "json": 1,
        }

        params = self._add_api_key(params)

        if page:
            params["pid"] = page
        if limit:
            params["limit"] = limit

        code, response = await self._get(self._root_url + "/index.php",
            params=params,
            **kwargs)

        res_list = list()
        for i in response:
            # some post may lacks "id" property,
            # default to "-1".
            res_list.append(GelbooruImage(str(i.get("id", "-1")), i))
        return res_list

    def _add_api_key(self, params: Dict[str, str]) -> Dict[str, str]:
        return self._fill_dict(params, {
            "user_id": self._user,
            "api_key": self._token,
        })


class Safebooru(Gelbooru):
    """Wrap API of Safebooru (https://safebooru.org/)

    Safebooru is the same as gelbooru,
    so we just inherit it.
    """
    pass

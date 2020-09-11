from typing import Any, List, Optional, Union
from asyncio import AbstractEventLoop

from .booru import Booru, BooruImage

API_URL = "https://danbooru.donmai.us/"


class DanbooruImage(BooruImage):
    def __init__(self, iid, data_dict):
        super().__init__(iid, data_dict)

    @property
    def author(self) -> Union[str, None]:
        return self._data_dict.get("author", None)

    @property
    def file_url(self) -> Union[str, None]:
        return self._data_dict.get("file_url", None)

    @property
    def rating(self) -> Union[str, None]:
        return self._data_dict.get("rating", None)


class Danbooru(Booru):
    """
    Wrap API of danbooru (https://danbooru.donmai.us/)

    See also: https://danbooru.donmai.us/wiki_pages/help:api

    Example:

    ```
    danbooru = Danbooru(username="username", api_key="your-api-key")
    danbooru.get_posts(limit=10, tags="yazawa_niko*")
    ```

    Note: It is recommanded that testing script on https://testbooru.donmai.us

    You can specify the url when you are creating an instance

    ```
    # specify api_url without trailing slash `/`
    danbooru = Danbooru(api_url="https://testbooru.donmai.us")
    danbooru.get_posts()
    ```

    """

    def __init__(
        self,
        username: str = None,
        api_key: str = None,
        api_url: str = API_URL,
        loop: Optional[AbstractEventLoop] = None,
    ):
        super(Danbooru, self).__init__(loop)
        self._username = username
        self._api_key = api_key
        self._api_url = api_url

    async def get_posts(
        self,
        tags: str = "",
        page: int = None,
        limit: int = None,
        md5: str = None,
        random: bool = True,
        raw: bool = False,
        **kwargs,
    ) -> List[DanbooruImage]:
        """get a list of posts. API: /posts.json

        Args:
            tags (str, optional): The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags. Defaults to "".
            page (int, optional): The page number. Defaults to None.
            limit (int, optional): How many posts you want to retrieve. Defaults to None.
            md5 (str, optional): The md5 of the image to search for. Defaults to None.
            random (bool, optional): Can be: true, false Defaults to True.
            raw (bool, optional): When this parameter is set the tags parameter will not be parsed for aliased tags, metatags or multiple tags, and will instead be parsed as a single literal tag. Defaults to False.

        Returns:
            List[DanbooruImage]: a list contains `DanbooruImage`
        """

        params: List[str, Any] = {
            "tags": tags,
            "random": 1 if random else 0,
            "raw": 1 if raw else 0,
        }

        if page: params["page"] = page
        if limit: params["limit"] = limit
        if md5:
            params["md5"] = md5
            del params["tags"]

        code, response = await self._get(
            self._api_url + "/posts.json", params=params, **kwargs,
        )

        res_list = list()
        for i in response:
            # some post may lacks "id" property,
            # default to "0".
            res_list.append(DanbooruImage(i.get("id", "-1"), i))
        return res_list

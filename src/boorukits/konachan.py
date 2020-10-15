from asyncio import AbstractEventLoop
from typing import List, Optional, Union

from .booru import Booru, BooruImage

API_URL = "https://konachan.net/"
R18_API_URL = "https://konachan.com/"


class KonachanImage(BooruImage):

    def __init__(self, iid, data_dict):
        super().__init__(iid, data_dict)

    @property
    def thumbnail_url(self) -> str:
        return self._data_dict.get("preview_url", "")


class Konachan(Booru):
    """
    Wrap API of Konachan (https://konachan.net/)

    See also: https://konachan.com/help/api

    Example:

    ```
    Konachan = Konachan(user="username", token="your-api-key")
    Konachan.get_posts(limit=10, tags="yazawa_niko*")
    ```
    """

    def __init__(
        self,
        user: str = None,
        token: str = None,
        root_url: str = API_URL,
        proxy: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None,
    ):
        """Create an instance of Konachan.

        The default URL root is https://konachan.net/ .

        You can also specify other URL by passing `root_url` parameter.

        Args:
            user (str, optional): User name/id of Konachan. Defaults to None.
            token (str, optional): API Key of Konachan. Defaults to None.
            root_url (str, optional): API URL root. Defaults to API_URL.
            loop (Optional[AbstractEventLoop], optional): EventLoop. Defaults to None.
        """
        super(Konachan, self).__init__(proxy=proxy, loop=loop)
        self._user = user
        self._token = token
        self._root_url = root_url

    async def get_post(self, id: str) -> Union[KonachanImage, None]:
        """Get a specific post by id.
        API: /posts/$id.json (when $id is the post id)

        Args:
            id (str): The post id

        Returns:
            Union[KonachanImage, None]: KonachanImage
        """
        response = await self.get_posts(tags=f"id:{id}")

        if len(response) >= 1:
            return response[0]
        return None

    async def get_posts(
        self,
        tags: str = "",
        page: int = None,
        limit: int = None,
        **kwargs,
    ) -> List[KonachanImage]:
        """Get a list of posts. API: /posts.json

        Args:
            tags (str, optional): The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags. Defaults to "".
            page (int, optional): The page number. Defaults to None.
            limit (int, optional): How many posts you want to retrieve. Defaults to None.

        Returns:
            List[KonachanImage]: a list contains `KonachanImage`
        """

        params = {
            "tags": tags,
            # api key
            "login": self._user,
            "api_key": self._token,
            # other possible parameters
            "page": page,
            "limit": limit,
        }

        code, response = await self._get(
            self._root_url + "/post.json",
            params=params,
            **kwargs,
        )

        res_list = list()
        for i in response:
            # some post may lacks "id" property,
            # default to "-1".
            res_list.append(KonachanImage(str(i.get("id", "-1")), i))
        return res_list

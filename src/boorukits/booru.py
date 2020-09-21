"""
Base class for *booru-like gallary
"""
from asyncio import AbstractEventLoop
from json import JSONDecodeError
from typing import Any, Dict, List, Optional, Tuple, Union

from aiohttp import ClientSession


class Booru:
    """General class wrapping *booru-like gallary website API.

    """

    def __init__(
        self,
        loop: Optional[AbstractEventLoop] = None,
    ):
        self._loop = loop

    async def _get(
        self,
        url: str,
        params: Dict[str, str] = None,
        headers: Dict[str, str] = None,
        data: Dict[str, str] = None,
        **kwargs,
    ) -> Tuple[int, Union[Dict[str, str], None]]:
        """Send an HTTP GET request

        Args:
            url (str): URL in string
            params (Dict[str, str], optional): url params. Defaults to None.
            headers (Dict[str, str], optional): http headers. Defaults to None.
            data (Dict[str, str], optional): http body data. Defaults to None.

        Returns:
            Tuple[int, Union[Dict[str, str], None]]: tuple with response status code and returned JSON data.
        """
        return await self._request("get",
            url,
            params=params,
            headers=headers,
            data=data,
            **kwargs)

    async def _post(
        self,
        url: str,
        params: Dict[str, str] = None,
        headers: Dict[str, str] = None,
        data: Dict[str, str] = None,
        **kwargs,
    ) -> Tuple[int, Union[Dict[str, str], None]]:
        """Send an HTTP POST request

        Args:
            url (str): URL in string
            params (Dict[str, str], optional): url params. Defaults to None.
            headers (Dict[str, str], optional): http headers. Defaults to None.
            data (Dict[str, str], optional): http body data. Defaults to None.

        Returns:
            Tuple[int, Union[Dict[str, str], None]]: tuple with response status code and returned JSON data.
        """
        return await self._request("post",
            url,
            params=params,
            headers=headers,
            data=data,
            **kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        params: Dict[str, str] = None,
        headers: Dict[str, str] = None,
        data: Dict[str, str] = None,
        **kwargs,
    ) -> Tuple[int, Union[Dict[str, str], None]]:
        """Send an HTTP request

        Args:
            method (str): HTTP method (GET, POST, PUT...)
            url (str): URL in string
            params (Dict[str, str], optional): url params. Defaults to None.
            headers (Dict[str, str], optional): http headers. Defaults to None.
            data (Dict[str, str], optional): http body data. Defaults to None.

        Returns:
            Tuple[int, Union[Dict[str, str], None]]: tuple with response status code and returned JSON data.
        """
        async with ClientSession(loop=self._loop) as session:
            async with session.request(method,
                url,
                params=params,
                headers=headers,
                **kwargs) as response:
                try:
                    return response.status, await response.json()
                except JSONDecodeError:
                    return response.status, None


class BooruImage:

    def __init__(
        self,
        iid: str,
        data_dict: Dict[str, Any],
    ):
        self.id = iid
        self._data_dict = data_dict

    @property
    def author(self) -> str:
        """Return author of current image.

        name can be English or Japanese? (depends on website)

        Perhaps return empty string.

        Returns:
            str: author name
        """
        return self._data_dict.get("author", "")

    @property
    def file_url(self) -> str:
        """Return download-able url of current image.

        `file_url` is always the largest size of current image.

        If you want a smaller or thumbnail version,
        please consider `thumbnail_url` or `sample_url`.

        Returns:
            str,: Image file url
        """
        return self._data_dict.get("file_url", "")

    @property
    def rating(self) -> Union[str, None]:
        """Return rating of current image.

        Values can be `s` for safe, `q` for questionaire and `e` for exciplit.

        Returns:
            Union[str, None]: rating
        """
        return self._data_dict.get("rating", None)

    @property
    def sample_url(self) -> str:
        """Return download-able url of current image.

        Returns:
            str,: Image sample url
        """
        return self._data_dict.get("sample_url", "")

    @property
    def source(self) -> str:
        """Return source url of current image.

        In some gallery website, if this image was from a manga,
        it might return the name of the manga.

        In some case, source would be empty string.

        Returns:
            str: source url
        """
        return self._data_dict.get("source", "")

    @property
    def tags(self) -> str:
        """Return tags of current image.

        Tags are always splited by spaces

        Returns:
            str: tags
        """
        return self._data_dict.get("tags", "")

    @property
    def tags_list(self) -> List[str]:
        """Return tag list of current image.

        Returns:
            List[str]: tag list
        """
        return self.tags.split()

    @property
    def thumbnail_url(self) -> str:
        """Return download-able thumbnail url of current image.

        Returns:
            str,: Image thumbnail url
        """
        return self._data_dict.get("thumbnail_url", "")

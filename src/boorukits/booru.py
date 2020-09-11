"""
Base class for *booru-like gallary
"""
from typing import Any, Dict, Optional, Tuple, Union
from asyncio import AbstractEventLoop
from json import JSONDecodeError

from aiohttp import ClientSession


class Booru:
    """General class wrapping *booru-like gallary website API.

    """

    def __init__(
        self, loop: Optional[AbstractEventLoop] = None,
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
        return await self._request(
            "get", url, params=params, headers=headers, data=data, **kwargs
        )

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
        return await self._request(
            "post", url, params=params, headers=headers, data=data, **kwargs
        )

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
            async with session.request(
                method, url, params=params, headers=headers, **kwargs
            ) as response:
                try:
                    return response.status, await response.json()
                except JSONDecodeError:
                    return response.status, None


class BooruImage:
    def __init__(
        self, iid: str, data_dict: Dict[str, Any],
    ):
        self.id = iid
        self._data_dict = data_dict

    @property
    def author(self) -> Union[str, None]:
        """Return author of current image.

        name can be English or Japanese? (depends on website)

        Perhaps return None or empty string.

        Returns:
            Union[str, None]: author name
        """
        return None

    @property
    def file_url(self) -> Union[str, None]:
        """Return download-able url of current image.

        Returns:
            Union[str, None]: Image file url
        """
        return None

    @property
    def rating(self) -> Union[str, None]:
        """Return rating of current image.

        Values can be `s` for safe, `q` for questionaire and `e` for exciplit.

        Returns:
            Union[str, None]: rating
        """
        return None

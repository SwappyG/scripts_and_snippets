from __future__ import annotations

from typing import Any, Optional, TypeVar
from types import TracebackType
import requests
from pydantic import BaseModel

from .fastapi_server_exceptions import raise_if_error
from .fastapi_endpoints import HEARTBEAT_HEALTH_EP

T = TypeVar("T", bound=BaseModel)


class FastAPIClientBase:
    """This helps you connect to and communicate with a fastapi server
    User should inherit from this class, implement specific endpoint functions and
    use the _get, _post, etc methods to make calls"""

    def __init__(
        self, host: str, port: int, *, prefix: str = "", timeout: float = 30.0
    ):
        self._host = host
        self._port = int(port)
        self._addr = f"http://{host}:{port}/{prefix}"
        self._timeout = timeout
        self._session = requests.Session()

        # By making a call, we ensure that there's a connection with the server
        _resp = self._get(HEARTBEAT_HEALTH_EP)

    def __enter__(self) -> FastAPIClientBase:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException],
        exception_value: BaseException,
        exception_traceback: TracebackType,
    ):
        self.stop()

    def stop(self) -> None:
        """close the connection. This instance cannot be used after"""
        try:
            self._session.close()
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    @property
    def base_url(self) -> str:
        """get the address of the server as a url"""
        return self._addr

    @property
    def port(self) -> int:
        """the port that all requests will be made to"""
        return self._port

    @property
    def host(self) -> str:
        """the host (ip address) that all requests will be made to"""
        return self._host

    def _get(self, path: str, params: Optional[T] = None) -> requests.Response:
        try:
            resp = self._session.get(
                f"{self._addr}{path}",
                params=self.__dump_model(params),
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"failed to make GET request to {self._addr}{path}"
            ) from e
        raise_if_error(resp)
        return resp

    def _post(self, path: str, basemodel: Optional[T] = None) -> requests.Response:
        try:
            resp = self._session.post(
                f"{self._addr}{path}",
                json=self.__dump_model(basemodel),
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"failed to make POST request to {self._addr}{path}"
            ) from e
        raise_if_error(resp)
        return resp

    def _put(self, path: str, basemodel: Optional[T] = None) -> requests.Response:
        try:
            resp = self._session.put(
                f"{self._addr}{path}",
                json=self.__dump_model(basemodel),
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"failed to make PUT request to {self._addr}{path}"
            ) from e

        raise_if_error(resp)
        return resp

    def _patch(self, path: str, basemodel: Optional[T] = None) -> requests.Response:
        try:
            resp = self._session.patch(
                f"{self._addr}{path}",
                json=self.__dump_model(basemodel),
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"failed to make PATCH request to {self._addr}{path}"
            ) from e
        raise_if_error(resp)
        return resp

    def _delete(self, path: str, basemodel: Optional[T] = None) -> requests.Response:
        try:
            resp = self._session.delete(
                f"{self._addr}{path}",
                json=self.__dump_model(basemodel),
                timeout=self._timeout,
            )
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(
                f"failed to make DELETE request to {self._addr}{path}"
            ) from e
        raise_if_error(resp)
        return resp

    @staticmethod
    def __dump_model(maybe_model: Optional[T]) -> Optional[dict[str, Any]]:
        if maybe_model:
            return maybe_model.model_dump()
        return None

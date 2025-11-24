import threading
import time
import logging
import uvicorn
from fastapi import FastAPI
from types import TracebackType

logger = logging.getLogger(__name__)
logger.setLevel(level="INFO")


class UvicornServer:
    def __init__(self, app: FastAPI, host: str, port: int, log_level: str = "info", start_timeout: float=10.0):
        self.config = uvicorn.Config(app, host=host, port=port, log_level=log_level)
        self.server = uvicorn.Server(self.config)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        # Block until server has started binding
        start_time = time.time()
        while not self.server.started:
            if time.time() - start_time > start_timeout:
                self.stop()
                raise RuntimeError(f"Failed to start server in {start_timeout=} secs")
            logger.debug("waiting for server to start..")
            time.sleep(0.1)

        # once started, extract the port from the underlying socket(s)
        if not self.server.servers:
            self.stop()
            raise RuntimeError("Server supposedly started, but uvicorn.Server.servers is empty")
        
        sock = next(iter(self.server.servers)).sockets[0]
        self._bound_port = sock.getsockname()[1]

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type: type[BaseException],
        exception_value: BaseException,
        exception_traceback: TracebackType,
    ):
        self.stop()

    def stop(self, wait_timeout: float=5.0, reraise_on_failure: bool=False):
        """Stops the server"""
        # Ask uvicorn to exit and give the thread a moment to wind down
        self.server.should_exit = True
        # In case it's in a sleep/poll, also set 'force_exit' on next loop
        self.server.force_exit = True
        try:
            self.thread.join(timeout=wait_timeout)
        except RuntimeError as e:
            logger.error(f"failed to join uvicorn thread within {wait_timeout=} secs. Got {e=}")
            if reraise_on_failure:
                raise

    @property
    def bound_port(self) -> int:
        """Returns the port that the server is running on"""
        if self._bound_port is None:
            raise RuntimeError("Server not started yet")
        return self._bound_port

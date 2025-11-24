"""
This is useful when a single script needs to both provide a FastAPI server and
do other things (like a GUI, different server, etc)
"""

import argparse
from uvicorn_server_threaded import UvicornServer
from fastapi_server_async import app
import logging


logger = logging.getLogger(__name__)
logger.setLevel(level="INFO")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog=__file__, description="Run Recipe Manager HTTP server + Qt event loop"
    )
    parser.add_argument(
        "--host",
        nargs="?",
        default="localhost",
        help="host address (like 'localhost' or '127.0.0.1') for the fastapi server",
        required=False,
        type=str
    )
    parser.add_argument(
        "--port",
        help="port number for the fastapi server",
        nargs="?",
        default=0,  # 0 means that a random port will be selected
        required=False,
        type=int,
    )
    args = parser.parse_args()

    # This starts the server
    with UvicornServer(
        app=app, host=args.host, port=args.port
    ) as srv:
        logger.info(f"Server running on {srv.bound_port}")

        # Do whatever else needs to happen here, or just sit in a loop and wait for 
        # KeyboardInterrupt

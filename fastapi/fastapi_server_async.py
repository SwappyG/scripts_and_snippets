from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .fastapi_server_exceptions import (
    NotFoundException,
    StateException,
    PreemptedException,
    RequestValidationError,
    make_json_response,
)

from .fastapi_endpoints import (
    router,
    heartbeat_router,
    API_PREFIX,
    HEARTBEAT_ROUTER_PREFIX,
)

FASTAPI_APP_NAME = "MyFastApiApp"

# Add any localhost:<port> / 127.0.0.1:<port> / 0.0.0.0:<port> that are allowed here
ALLOWED_ORIGINS: list[str] = []

# This should cover most bases, but add any other HTTP Verbs here
ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# This should be updated with info about how to handle http vs https
ALLOW_CREDENTIALS = False

# This limits the types of headers. For production use, this should be specified.
ALLOWED_HEADERS = ["*"]


@asynccontextmanager
async def _lifespan(_fastapi_app: FastAPI):
    # Add items to fastapi_app.state.<anything> here
    yield
    # Clean up anything added to fastapi_app.state.<anything>


app = FastAPI(title=FASTAPI_APP_NAME, lifespan=_lifespan)
app.include_router(router, prefix=API_PREFIX)
app.include_router(heartbeat_router, prefix=HEARTBEAT_ROUTER_PREFIX)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)


@app.exception_handler(ValueError)
async def _value_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: ValueError
) -> JSONResponse:
    return make_json_response(422, exc)


@app.exception_handler(KeyError)
async def _key_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: KeyError
) -> JSONResponse:
    return make_json_response(422, exc)


@app.exception_handler(IndexError)
async def _index_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: IndexError
) -> JSONResponse:
    return make_json_response(422, exc)


@app.exception_handler(StateException)
async def _state_exception_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: StateException
) -> JSONResponse:
    return make_json_response(409, exc)


@app.exception_handler(NotFoundException)
async def _not_found_exception_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: NotFoundException
) -> JSONResponse:
    return make_json_response(404, exc)


@app.exception_handler(PermissionError)
async def _permission_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: PermissionError
) -> JSONResponse:
    return make_json_response(403, exc)


@app.exception_handler(TimeoutError)
async def _timeout_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: TimeoutError
) -> JSONResponse:
    return make_json_response(504, exc)


@app.exception_handler(RuntimeError)
async def _runtime_error_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: RuntimeError
) -> JSONResponse:
    return make_json_response(500, exc)


@app.exception_handler(RequestValidationError)
async def _validation_exception_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return make_json_response(422, exc)


@app.exception_handler(PreemptedException)
async def _preempted_exception_handler(  # pyright: ignore[reportUnusedFunction]
    _request: Request, exc: PreemptedException
) -> JSONResponse:
    return make_json_response(409, exc)

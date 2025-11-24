import typing as t
from pydantic import BaseModel
from fastapi.routing import APIRouter

# Add some common endpoints by default so client can ensure we're alive 
heartbeat_router = APIRouter()
HEARTBEAT_ROUTER_PREFIX = '/heartbeat'
HEARTBEAT_HEALTH_EP = HEARTBEAT_ROUTER_PREFIX + "/health"
HEARTBEAT_ECHO_EP = HEARTBEAT_ROUTER_PREFIX + "/echo"

# This should contain user defined endpoints. 
# Add as many as you like. Move to diff files. Give them all a unique prefix
router = APIRouter()
API_PREFIX = "/api"


class HealthReply(BaseModel):
    pass

class EchoReply(BaseModel):
    echo: dict[str, t.Any]


@heartbeat_router.get('/health', response_model=HealthReply)
def _health_endpoint( # pyright: ignore[reportUnusedFunction]
    _args: t.Any
):
    return HealthReply()

@heartbeat_router.get('/echo', response_model=HealthReply)
def _echo_endpoint( # pyright: ignore[reportUnusedFunction]
    args: dict[str, t.Any]
):
    return EchoReply(echo=args)
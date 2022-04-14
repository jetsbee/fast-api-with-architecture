from fastapi import APIRouter

from ..logging import ErrorLoggingRoute

router = APIRouter(route_class=ErrorLoggingRoute)

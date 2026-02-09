from fastapi import Request, status, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.ventio_api.infrastructure.auth.security import decode_token
from src.ventio_api.exceptions import InvalidToken
from typing import Callable, Awaitable


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        public_paths = ["/signin", "/signup", "/docs", "/openapi.json"]

        if request.url.path in public_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid credentials"},
            )

        try:
            token = auth_header.split(" ")[1]
            token_data = decode_token(token, expected_type="access")

            request.state.user_id = token_data.user_id
            request.state.name = token_data.name

        except InvalidToken as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(e)}
            )

        return await call_next(request)

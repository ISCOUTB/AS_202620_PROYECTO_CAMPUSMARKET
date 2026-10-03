"""Presupuesto del proceso: trabajo intensivo serial y cuerpos HTTP acotados."""
from threading import BoundedSemaphore

from fastapi import HTTPException
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

HEAVY_WORK_SLOT = BoundedSemaphore(1)
MAX_JSON_BODY = 64 * 1024
MAX_MULTIPART_BODY = 6 * 1024 * 1024


class RequestBodyLimitMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        content_type = headers.get(b"content-type", b"").lower()
        limit = MAX_MULTIPART_BODY if content_type.startswith(b"multipart/form-data") else MAX_JSON_BODY
        detail = "La solicitud supera el límite permitido."
        try:
            declared = int(headers.get(b"content-length", b"0"))
        except ValueError:
            declared = 0
        if declared > limit:
            await JSONResponse(status_code=413, content={"detail": detail})(scope, receive, send)
            return
        received = 0

        async def limited_receive():
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > limit:
                    raise HTTPException(status_code=413, detail=detail)
            return message

        await self.app(scope, limited_receive, send)

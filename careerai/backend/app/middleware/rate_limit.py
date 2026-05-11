from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from collections import defaultdict
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self._store = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        self._store[ip] = [t for t in self._store[ip] if now - t < self.window]
        if len(self._store[ip]) >= self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        self._store[ip].append(now)
        return await call_next(request)

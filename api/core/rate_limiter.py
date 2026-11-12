import os

from slowapi import Limiter
from slowapi.util import get_remote_address

# Per-client-IP limit; override with the RATE_LIMIT env var (e.g. "120/minute")
DEFAULT_LIMIT = os.getenv("RATE_LIMIT", "60/minute")

# Applied per route with @limiter.limit(DEFAULT_LIMIT)
limiter = Limiter(key_func=get_remote_address)

from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a limiter instance that will use the client's IP address as the key
limiter = Limiter(key_func=get_remote_address)

# Default rate limit settings
RATE_LIMIT_PER_MINUTE = 10  # Requests per minute
RATE_LIMIT_PER_DAY = 1000   # Requests per day

# Rate limit decorator configurations
DEFAULT_LIMIT = f"{RATE_LIMIT_PER_MINUTE}/minute"
DAILY_LIMIT = f"{RATE_LIMIT_PER_DAY}/day" 
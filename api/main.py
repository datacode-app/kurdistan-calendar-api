from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.core.rate_limiter import limiter
from api.routes import holidays, calendar

app = FastAPI(
    title="Kurdistan Calendar API",
    description="An API providing access to Kurdish holidays, historical events, and cultural celebrations.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    """
    Root endpoint returning API information.
    Rate limited to 10 requests per minute.
    """
    return {
        "name": "Kurdistan Calendar API",
        "version": "1.0.0",
        "description": "Access Kurdish holidays, historical events, and cultural celebrations",
        "documentation": "/docs",
        "rate_limits": {
            "per_minute": 10,
            "per_day": 1000
        }
    }

# Include the holidays router
app.include_router(holidays.router)

# Include the calendar router
app.include_router(calendar.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
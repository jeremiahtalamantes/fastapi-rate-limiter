from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from token_bucket import TokenBucket  # Import the TokenBucket class

#
#
# BASIC RATE LIMITER USING FASTAPI
# USING TOKEN BUCKET ALGO
#
#

# Setup App
app = FastAPI()

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, bucket: TokenBucket):
        super().__init__(app)
        self.bucket = bucket  # Initialize the middleware with a token bucket

    async def dispatch(self, request: Request, call_next):
        # Process each incoming request
        if self.bucket.take_token():
            # If a token is available, proceed with the request
            return await call_next(request)
        # If no tokens are available, return a 429 error (rate limit exceeded)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

# Initialize the token bucket with 4 tokens capacity and refill rate of 2 tokens/second
bucket = TokenBucket(capacity=4, refill_rate=2)

# Add the rate limiting middleware to the FastAPI app
app.add_middleware(RateLimiterMiddleware, bucket=bucket)

@app.get("/")
async def read_root():
    # A sample endpoint to demonstrate the rate limiter in action
    return {"message": "Hello World"}

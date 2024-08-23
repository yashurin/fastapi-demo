from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from collections import deque
import time
import asyncio
import logging

app = FastAPI()

request_times = deque()
message_sizes = deque()

@app.post("/rate")
async def root(request: Request):
    logging.info('Inside the endpoint')

    # Record the timestamp and size of the incoming request
    current_time = time.time()
    body = await request.body()
    message_size = len(body)

    request_times.append(current_time)
    message_sizes.append(message_size)

    # Remove timestamps and sizes older than 1 second
    while request_times and current_time - request_times[0] > 1:
        request_times.popleft()
        message_sizes.popleft()

    # Calculate the rate of requests per second and the total size of messages
    request_rate = len(request_times)
    total_message_size = sum(message_sizes)

    return JSONResponse(content={
        "request_rate_per_second": request_rate,
        "total_message_size_per_second": total_message_size,
        "single_message_size": message_size
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use the PORT environment variable if available
    uvicorn.run(app, host="0.0.0.0", port=port)



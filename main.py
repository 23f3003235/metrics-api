import time
import uuid
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-2dd4k1.example.com"
EMAIL = "23f3003235@ds.study.iitm.ac.in"


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN], 
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

class TimingAndIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()               
        request_id = str(uuid.uuid4())         

        response = await call_next(request)     

        process_time = time.time() - start_time 
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

app.add_middleware(TimingAndIDMiddleware)

@app.get("/stats")
def get_stats(values: str = Query(..., description="Comma-separated integers")):
    # Parse "1,2,3" into [1, 2, 3]
    nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    return JSONResponse({
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean,
    })
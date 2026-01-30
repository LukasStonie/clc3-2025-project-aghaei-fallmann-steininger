import random
import numpy as np

from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time, psutil

from sqlalchemy.orm import Session

from . import models
from . import database

models.Base.metadata.create_all(bind=database.engine)

class TicketPurchase(BaseModel):
    user_id: str
    quantity: int

class Concert(BaseModel):
    title: str
    date: str
    venue: str
    number_of_tickets: int


# In your FastAPI route:
def buy_ticket(concert_id: int, db: Session):
    sold_count = db.query(models.TicketPurchase).filter(models.TicketPurchase.concert_id == concert_id).count()

    concert = db.query(models.Concert).filter(models.Concert.id == concert_id).first()

    if sold_count < concert.total_capacity:
        new_ticket = models.TicketPurchase(concert_id=concert_id, user_email="")
        db.add(new_ticket)
        db.commit()
    else:
        return "Sold out!"
app = FastAPI()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("request_duration_seconds", "Request duration in seconds")
CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage percent")
MEMORY_USAGE = Gauge("memory_usage_percent", "Memory usage percent")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    REQUEST_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
    REQUEST_DURATION.observe(duration)
    return response

@app.post("/buy/{concert_id}")
def buy_tickets(concert_id: int, purchase: models.TicketPurchase):

    deny = np.random.randint(low=0, high=1000)

    if deny > 900:
        print(f" Denying ticket purchase for concert {concert_id} ")
        return HTTPException(status_code=409, detail="Tickets currently unavailable")

    # Simulate ticket purchasing logic
    time_to_sleep = np.random.randint(1,50)
    time.sleep(time_to_sleep)
    return {"concert_id": concert_id, "quantity": purchase.quantity, "status": "success"}

@app.post("/concerts/new")
def create_concert(Concert: models.Concert):
    # Simulate concert creation logic
    return {"title": Concert.title, "status": "created"}

@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return Response(generate_latest(), media_type="text/plain")
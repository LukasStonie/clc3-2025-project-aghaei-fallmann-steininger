import random
import time
from contextlib import asynccontextmanager

import numpy as np
import psutil
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

# Assuming database.py has a 'get_db' generator and 'engine'
from . import database, models


# --- 1. Lifespan for Table Initialization ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This creates the tables if they don't exist yet
    database.Base.metadata.create_all(bind=database.engine)
    yield


# --- 2. Pydantic Models (Schemas) ---
# Use these for Request Bodies, NOT the SQLAlchemy models
class TicketPurchaseSchema(BaseModel):
    user_email: str
    quantity: int


class ConcertSchema(BaseModel):
    title: str
    date: str
    venue: str
    number_of_tickets: int


# --- 3. Initialize App with Lifespan ---
app = FastAPI(lifespan=lifespan)

# Metrics setup (Unchanged)
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", [
                        "method", "endpoint", "status"])
REQUEST_DURATION = Histogram(
    "request_duration_seconds", "Request duration in seconds")
CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage percent")
MEMORY_USAGE = Gauge("memory_usage_percent", "Memory usage percent")


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    REQUEST_COUNT.labels(request.method, request.url.path,
                         str(response.status_code)).inc()
    REQUEST_DURATION.observe(duration)
    return response


# --- 4. Logic Extraction ---
# I moved the logic inside the route to make sure it actually runs


def process_purchase(concert_id: int, purchase: TicketPurchaseSchema, db: Session):
    # 1. Calculate how many tickets are already sold
    # .scalar() returns None if no tickets are sold, so we use 'or 0' to fix that
    sold_count = db.query(func.sum(models.TicketPurchase.quantity)) \
        .filter(models.TicketPurchase.concert_id == concert_id) \
        .scalar() or 0

    # 2. Get the concert to check its max capacity
    concert = db.query(models.Concert).filter(
        models.Concert.id == concert_id).first()

    if not concert:
        return False

    # 3. Check if there is enough space left
    if (sold_count + purchase.quantity) <= concert.total_capacity:
        # Create the new ticket record
        # Note: We map 'user_id' from the schema to 'user_email' in the DB model
        new_ticket = models.TicketPurchase(
            concert_id=concert_id,
            user_email=purchase.user_email,
            quantity=purchase.quantity
        )

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)  # Optional: loads the new ID into the object
        return True

    # 4. Not enough space
    return False


# --- 5. Routes with Dependency Injection ---

@app.post("/buy_random_deny/{concert_id}")
def buy_tickets_failing(
        concert_id: int,
        # Use Pydantic Schema here, not models.TicketPurchase
        purchase: TicketPurchaseSchema,
        db: Session = Depends(database.get_db)  # Inject DB Session
):
    try:
        # Random denial logic
        deny = np.random.randint(low=0, high=1000)
        if deny > 900:
            print(f" Denying ticket purchase for concert {concert_id} ")
            return JSONResponse(status_code=409, content={"message": "Tickets currently unavailable"})

        # Simulate delay
        # Reduced to 5 for testing speed
        time_to_sleep = np.random.randint(1, 5)
        time.sleep(time_to_sleep)

        # Example of actually using the DB (optional)
        success = process_purchase(concert_id, purchase, db)

        if not success:
            return JSONResponse(status_code=404, content={"message": "Concert sold out"})
        else:
            return {"concert_id": concert_id, "quantity": purchase.quantity, "status": "success"}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post("/buy/{concert_id}")
def buy_tickets(
        concert_id: int,
        # Use Pydantic Schema here, not models.TicketPurchase
        purchase: TicketPurchaseSchema,
        db: Session = Depends(database.get_db)  # Inject DB Session
):
    try:
        # Simulate delay
        # Reduced to 5 for testing speed
        time_to_sleep = np.random.randint(1, 5)
        time.sleep(time_to_sleep)

        # Example of actually using the DB (optional)
        success = process_purchase(concert_id, purchase, db)

        if not success:
            return JSONResponse(status_code=404, content={"message": "Concert sold out"})
        else:
            return {"concert_id": concert_id, "quantity": purchase.quantity, "status": "success"}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post("/concerts/new")
def create_concert(
        concert: ConcertSchema,  # Use Pydantic Schema
        db: Session = Depends(database.get_db)
):
    try:
        # Create the SQLAlchemy model instance using data from the Pydantic schema
        new_concert = models.Concert(
            title=concert.title,
            date=concert.date,
            venue=concert.venue,
            total_capacity=concert.number_of_tickets
        )

        db.add(new_concert)
        db.commit()
        db.refresh(new_concert)

        return {"title": new_concert.title, "status": "created", "id": new_concert.id}
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": str(err)})


@app.get("/concerts")
def get_all_available_concerts(db: Session = Depends(database.get_db)):

    try:
        concerts = db.query(models.Concert.id).all()

        # Manually transforming the SQLAlchemy objects into a list of dictionaries
        return [
            {
                "id": c.id
            } for c in concerts
        ]
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": str(err)})


@app.get("/health")
def health_check():
    return Response(content="", media_type="text/plain")


@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    return Response(generate_latest(), media_type="text/plain")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx, os

app = FastAPI(
    title="Order Service",
    description="Manages orders for the K11 platform. Consumes user-service to attach user profiles.",
    version="1.0.0",
)

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")


class Order(BaseModel):
    id: str
    user_id: str
    items: list[str]
    total: float
    status: str = "pending"


class CreateOrder(BaseModel):
    user_id: str
    items: list[str]
    total: float


@app.get("/api/v1/orders", response_model=list[Order], tags=["orders"])
async def list_orders(page: int = 1):
    """List all orders."""
    return []


@app.get("/api/v1/orders/{id}", response_model=Order, tags=["orders"])
async def get_order(id: str):
    """Get an order by ID."""
    raise HTTPException(status_code=404, detail="Order not found")


@app.post("/api/v1/orders", response_model=Order, status_code=201, tags=["orders"])
async def create_order(body: CreateOrder):
    """Create a new order. Validates the user exists via user-service."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{USER_SERVICE_URL}/api/v2/users/{body.user_id}")
        if resp.status_code == 404:
            raise HTTPException(status_code=422, detail="User not found")
    return Order(id="generated-id", **body.model_dump())


@app.patch("/api/v1/orders/{id}", response_model=Order, tags=["orders"])
async def update_order_status(id: str, status: str):
    """Update order status."""
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "order-service", "version": "1.0.0"}

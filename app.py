from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import Driver, Order, Location
from services import DispatchSystem

app = FastAPI(title="Dispatch System API")

system = DispatchSystem()


class LocationInput(BaseModel):
    x: float
    y: float


class DriverCreateRequest(BaseModel):
    id: str
    location: LocationInput


class OrderCreateRequest(BaseModel):
    id: str
    pickup: LocationInput
    dropoff: LocationInput


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/drivers")
def list_drivers():
    return [
        {
            "id": driver.id,
            "location": {
                "x": driver.location.x,
                "y": driver.location.y,
            },
            "status": str(driver.status),
        }
        for driver in system.drivers
    ]


@app.post("/drivers", status_code=201)
def create_driver(request: DriverCreateRequest):
    existing_driver = system.get_driver_by_id(request.id)
    if existing_driver is not None:
        raise HTTPException(status_code=400, detail="Driver already exists")

    driver = Driver(
        id=request.id,
        location=Location(x=request.location.x, y=request.location.y),
    )
    system.add_driver(driver)

    return {
        "message": "Driver created",
        "driver": {
            "id": driver.id,
            "location": {
                "x": driver.location.x,
                "y": driver.location.y,
            },
            "status": str(driver.status),
        },
    }


@app.get("/orders")
def list_orders():
    return [
        {
            "id": order.id,
            "pickup": {
                "x": order.pickup.x,
                "y": order.pickup.y,
            },
            "dropoff": {
                "x": order.dropoff.x,
                "y": order.dropoff.y,
            },
            "status": str(order.status),
            "assigned_driver_id": order.assigned_driver_id,
        }
        for order in system.orders
    ]


@app.post("/orders", status_code=201)
def create_order(request: OrderCreateRequest):
    existing_order = system.get_order_by_id(request.id)
    if existing_order is not None:
        raise HTTPException(status_code=400, detail="Order already exists")

    order = Order(
        id=request.id,
        pickup=Location(x=request.pickup.x, y=request.pickup.y),
        dropoff=Location(x=request.dropoff.x, y=request.dropoff.y),
    )
    system.create_order(order)

    return {
        "message": "Order created",
        "order": {
            "id": order.id,
            "pickup": {
                "x": order.pickup.x,
                "y": order.pickup.y,
            },
            "dropoff": {
                "x": order.dropoff.x,
                "y": order.dropoff.y,
            },
            "status": str(order.status),
            "assigned_driver_id": order.assigned_driver_id,
        },
    }


@app.post("/dispatch")
def dispatch_orders():
    system.dispatch_pending_orders()
    return {"message": "Dispatch finished"}


@app.post("/orders/{order_id}/complete")
def complete_order(order_id: str):
    order = system.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    system.complete_order(order)
    return {
        "message": f"Order {order_id} completed",
        "order": {
            "id": order.id,
            "status": str(order.status),
            "assigned_driver_id": order.assigned_driver_id,
        },
    }
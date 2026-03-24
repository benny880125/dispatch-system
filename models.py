from dataclasses import dataclass
from typing import Optional
from enum import Enum

class DriverStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"

class OrderStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

@dataclass
class Location:
    x: float
    y: float

@dataclass
class Driver:
    id: str
    location: Location
    status: DriverStatus = DriverStatus.IDLE

@dataclass
class Order:
    id: str
    pickup: Location
    dropoff: Location
    status: OrderStatus = OrderStatus.PENDING
    assigned_driver_id: Optional[str] = None
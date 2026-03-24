import math
from typing import List, Optional
from models import Driver, Order, Location, DriverStatus, OrderStatus

class DispatchSystem:
    def __init__(self):
        self.drivers: List[Driver] = []
        self.orders: List[Order] = []
        
    def add_driver(self, driver: Driver):
        self.drivers.append(driver)
        print(f"Added driver {driver.id} at ({driver.location.x}, {driver.location.y})")
    
    def create_order(self, order: Order):
        self.orders.append(order)
        print(f"Created order {order.id} from ({order.pickup.x}, {order.pickup.y})")
        
    def assign_nearest_driver(self, order: Order) -> Optional[Driver]:
        idle_drivers = [d for d in self.drivers if d.status == DriverStatus.IDLE]
        
        if not idle_drivers:
            print("No available driver")
            return None
        
        nearest_driver = None
        min_distance = float("inf")
        
        for driver in self.drivers:
            dist = self._distance(driver.location, order.pickup)
            if dist < min_distance:
                min_distance = dist
                nearest_driver = driver
        
        if nearest_driver:
            nearest_driver.status = DriverStatus.BUSY
            order.status = OrderStatus.ASSIGNED
            order.assigned_driver_id = nearest_driver.id
            
            print(f"Assigned driver {nearest_driver.id} to order {order.id}")
        
        return nearest_driver
    
    def complete_order(self, order: Order):
        if order.assigned_driver_id is None:
            print("Order has no driver assigned")
            return
        
        driver = next((d for d in self.drivers if d.id == order.assigned_driver_id), None)
        
        if driver:
            driver.status = DriverStatus.IDLE
            
        order.status = OrderStatus.COMPLETED
        print(f"Order {order.id} completed")
    
    def _distance(self, loc1: Location, loc2: Location) -> float:
        return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)
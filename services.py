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
        
    def get_driver_by_id(self, driver_id: str) -> Optional[Driver]:
        return next((d for d in self.drivers if d.id == driver_id), None)
    
    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return next((o for o in self.orders if o.id == order_id), None)
        
    def assign_nearest_driver(self, order: Order) -> Optional[Driver]:
        idle_drivers = [d for d in self.drivers if d.status == DriverStatus.IDLE]
        
        if not idle_drivers:
            print("No available driver")
            return None
        
        nearest_driver = None
        min_distance = float("inf")
        
        for driver in idle_drivers:
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
    
    def dispatch_pending_orders(self):
        for order in self.orders:
            if order.status == OrderStatus.PENDING:
                assigned_driver = self.assign_nearest_driver(order)
                if assigned_driver is None:
                    print(f"Order {order.id} is still pending")
    
    def complete_order(self, order: Order):
        if order.status == OrderStatus.COMPLETED:
            return
        
        if order.assigned_driver_id is None:
            print("Order has no driver assigned")
            return
        
        driver = self.get_driver_by_id(order.assigned_driver_id)
        
        if driver:
            driver.status = DriverStatus.IDLE
            
        order.status = OrderStatus.COMPLETED
        print(f"Order {order.id} completed")
    
    def complete_assigned_orders(self):
        for order in self.orders:
            if order.status == OrderStatus.ASSIGNED:
                self.complete_order(order)
    
    def print_current_status(self):
        print("=============Driver Status=============")
        for driver in self.drivers:
            print(f"Driver {driver.id} is currently {driver.status}")
        print("=============Order Status==============")
        for order in self.orders:
            print(f"Order {order.id} is currently {order.status}")
    
    def _distance(self, loc1: Location, loc2: Location) -> float:
        return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)
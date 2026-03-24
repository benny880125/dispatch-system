from models import Driver, Order, Location
from services import DispatchSystem


def main():
    system = DispatchSystem()

    system.add_driver(Driver("D1", Location(0, 0)))
    system.add_driver(Driver("D2", Location(5, 5)))
    system.add_driver(Driver("D3", Location(2, 1)))

    order1 = Order("O1", Location(1, 1), Location(8, 8))
    order2 = Order("O2", Location(6, 6), Location(9, 9))
    order3 = Order("O3", Location(0, 2), Location(3, 4))

    system.create_order(order1)
    system.create_order(order2)
    system.create_order(order3)

    system.dispatch_pending_orders()

    system.complete_assigned_orders()
    system.print_current_status()


if __name__ == "__main__":
    main()
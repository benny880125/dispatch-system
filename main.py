from models import Driver, Order, Location
from services import DispatchSystem


def main():
    system = DispatchSystem()

    system.add_driver(Driver("D1", Location(0, 0)))
    system.add_driver(Driver("D2", Location(5, 5)))
    system.add_driver(Driver("D3", Location(2, 1)))

    order1 = Order("O1", Location(1, 1), Location(8, 8))
    system.create_order(order1)

    system.assign_nearest_driver(order1)

    system.complete_order(order1)


if __name__ == "__main__":
    main()
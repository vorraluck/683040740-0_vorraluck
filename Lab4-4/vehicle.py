from abc import ABC, abstractmethod


class Vehicle(ABC):
    """
    Abstract base class for all vehicles.
    """

    def __init__(self, make, model, year):
        if year < 1886:
            raise ValueError("Invalid vehicle year")
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass

    def get_info(self):
        return f"{self.year} {self.make} {self.model}"


class CommercialVehicle:
    """
    Represents a commercial vehicle capable of carrying cargo.
    """

    def __init__(self, license_number, max_load):
        if max_load <= 0:
            raise ValueError("Max load must be positive")
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0

    def load_cargo(self, weight):
        if weight <= 0:
            return False
        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            return True
        return False

    def unload_cargo(self, weight):
        if weight >= self.current_load:
            self.current_load = 0
        else:
            self.current_load -= weight
        return self.current_load


class Car(Vehicle):
    """
    Passenger car class.
    """

    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def start_engine(self):
        self.is_running = True
        return "Car engine started"

    def stop_engine(self):
        self.is_running = False
        return "Car engine stopped"


class Trailer(CommercialVehicle):
    """
    Trailer for carrying loads.
    """

    def __init__(self, license_number, max_load, num_axles=2):
        super().__init__(license_number, max_load)
        if num_axles <= 0:
            raise ValueError("Number of axles must be positive")
        self.num_axles = num_axles

    def get_weight_per_axle(self):
        if self.num_axles == 0:
            return 0
        return self.current_load / self.num_axles


class DeliveryVan(Car, CommercialVehicle):
    """
    Delivery van using multiple inheritance.
    """

    def __init__(self, make, model, year, num_doors, license_number, max_load):
        Car.__init__(self, make, model, year, num_doors)
        CommercialVehicle.__init__(self, license_number, max_load)
        self.delivery_mode = False

    def toggle_delivery_mode(self):
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode {'ON' if self.delivery_mode else 'OFF'}"

    def get_info(self):
        return (
            f"{super().get_info()}, "
            f"License: {self.license_number}, "
            f"Load: {self.current_load}/{self.max_load}"
        )

    def begin_service(self):
        print(self.get_info())
        self.load_cargo(self.max_load * 0.5)
        print(self.start_engine())
        print(self.toggle_delivery_mode())
        print(self.stop_engine())
        self.unload_cargo(self.current_load)
        print(self.toggle_delivery_mode())

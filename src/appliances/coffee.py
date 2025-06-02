from src.appliances.base import Appliance


class ElectricMokaPot(Appliance):
    def __init__(self, cups=1, comfort_penalty=0.05, failure_rate=0.02, coffee_taste=0.78):
        super().__init__("ElectricMokaPot", comfort_penalty, failure_rate)
        self.cups = cups
        self._coffee_taste = coffee_taste

    def energy_consumption(self):
        return round(0.045 * self.cups, 3)

    def operation_time(self):
        return round(self.cups * 3, 1)

    def device_cost(self):
        return 300

    def coffee_taste(self):
        return self._coffee_taste

    def summary(self):
        data = super().summary()
        data["coffee_taste"] = self.coffee_taste()
        return data


class CoffeeMachine(Appliance):
    def __init__(self, cups=1, comfort_penalty=0.02, failure_rate=0.05, coffee_taste=0.9):
        super().__init__("CoffeeMachine", comfort_penalty, failure_rate)
        self.cups = cups
        self._coffee_taste = coffee_taste

    def energy_consumption(self):
        return round(0.08 * self.cups, 3)

    def operation_time(self):
        return round(self.cups * 1.5, 1)

    def device_cost(self):
        return 2000

    def coffee_taste(self):
        return self._coffee_taste

    def summary(self):
        data = super().summary()
        data["coffee_taste"] = self.coffee_taste()
        return data

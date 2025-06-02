from src.appliances.base import Appliance


class ThermomixTM6(Appliance):
    def __init__(self, recipe_complexity=1.0, comfort_penalty=0.05, failure_rate=0.04, cooking_quality=0.88):
        super().__init__("ThermomixTM6", comfort_penalty, failure_rate)
        self.recipe_complexity = recipe_complexity
        self._cooking_quality = cooking_quality

    def energy_consumption(self):
        return 0.75 * self.recipe_complexity  # kWh

    def operation_time(self):
        return 20 * self.recipe_complexity  # minutes

    def device_cost(self):
        return 5995  # PLN

    def cooking_quality(self):
        return self._cooking_quality

    def summary(self):
        data = super().summary()
        data["cooking_quality"] = self.cooking_quality()
        return data


class BoschCookit(Appliance):
    def __init__(self, recipe_complexity=1.0, comfort_penalty=0.07, failure_rate=0.05, cooking_quality=0.91):
        super().__init__("BoschCookit", comfort_penalty, failure_rate)
        self.recipe_complexity = recipe_complexity
        self._cooking_quality = cooking_quality

    def energy_consumption(self):
        return 0.9 * self.recipe_complexity  # nieco większa moc

    def operation_time(self):
        return 22 * self.recipe_complexity

    def device_cost(self):
        return 6399  # PLN

    def cooking_quality(self):
        return self._cooking_quality

    def summary(self):
        data = super().summary()
        data["cooking_quality"] = self.cooking_quality()
        return data

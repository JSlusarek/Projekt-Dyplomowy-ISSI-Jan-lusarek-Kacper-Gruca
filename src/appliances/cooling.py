from src.appliances.base import Appliance


class AirConditioner(Appliance):
    def __init__(self, duration_min=60, power_kw=1.5, comfort_penalty=0.01, failure_rate=0.1, cooling_quality=0.9):
        super().__init__("AirConditioner", comfort_penalty, failure_rate)
        self.duration_min = duration_min
        self.power_kw = power_kw
        self._cooling_quality = cooling_quality

    def energy_consumption(self):
        return self.power_kw * (self.duration_min / 60)

    def operation_time(self):
        return self.duration_min

    def device_cost(self):
        return 3000

    def cooling_quality(self):
        return self._cooling_quality

    def summary(self):
        data = super().summary()
        data["cooling_quality"] = self.cooling_quality()
        return data


class Fan(Appliance):
    def __init__(self, duration_min=60, power_kw=0.07, comfort_penalty=0.08, failure_rate=0.03, cooling_quality=0.4):
        super().__init__("Fan", comfort_penalty, failure_rate)
        self.duration_min = duration_min
        self.power_kw = power_kw
        self._cooling_quality = cooling_quality

    def energy_consumption(self):
        return self.power_kw * (self.duration_min / 60)

    def operation_time(self):
        return self.duration_min

    def device_cost(self):
        return 250

    def cooling_quality(self):
        return self._cooling_quality

    def summary(self):
        data = super().summary()
        data["cooling_quality"] = self.cooling_quality()
        return data

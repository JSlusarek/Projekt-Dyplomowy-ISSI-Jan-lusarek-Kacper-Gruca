from src.appliances.base import Appliance


class DesktopComputer(Appliance):
    def __init__(self, power_watt=150, daily_hours=6, comfort_penalty=0.02, failure_rate=0.03):
        super().__init__("DesktopComputer", comfort_penalty, failure_rate)
        self.power_kw = power_watt / 1000
        self.daily_hours = daily_hours
        self.price_kwh = 0.65
        self.co2_kwh = 0.4

    def energy_consumption(self):
        return self.power_kw * self.daily_hours

    def operation_time(self):
        return self.daily_hours * 60

    def device_cost(self):
        return 4000  # zł

    def cost(self):
        return round(self.energy_consumption() * self.price_kwh, 2)

    def co2_emission(self):
        return round(self.energy_consumption() * self.co2_kwh, 3)

    def computing_quality(self):
        return 0.95  # pełna wydajność CPU/GPU

    def summary(self):
        data = super().summary()
        data["computing_quality"] = self.computing_quality()
        return data


class LaptopWithMonitor(Appliance):
    def __init__(self, laptop_watt=40, monitor_watt=30, daily_hours=6,
                 comfort_penalty=0.01, failure_rate=0.05):
        super().__init__("LaptopWithMonitor", comfort_penalty, failure_rate)
        self.laptop_kw = laptop_watt / 1000
        self.monitor_kw = monitor_watt / 1000
        self.daily_hours = daily_hours
        self.price_kwh = 0.65
        self.co2_kwh = 0.4

    def energy_consumption(self):
        return (self.laptop_kw + self.monitor_kw) * self.daily_hours

    def operation_time(self):
        return self.daily_hours * 60

    def device_cost(self):
        return 5000  # laptop + monitor

    def cost(self):
        return round(self.energy_consumption() * self.price_kwh, 2)

    def co2_emission(self):
        return round(self.energy_consumption() * self.co2_kwh, 3)

    def computing_quality(self):
        return 0.85  # zależna od CPU klasy mobilnej

    def summary(self):
        data = super().summary()
        data["computing_quality"] = self.computing_quality()
        return data

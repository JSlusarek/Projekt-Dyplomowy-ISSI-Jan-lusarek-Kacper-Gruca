from src.appliances.base import Appliance


class LadderHeater(Appliance):
    def __init__(self, power_kw=1.0, usage_hours_per_day=2.0, comfort_penalty=0.03, failure_rate=0.04):
        super().__init__("LadderHeater", comfort_penalty, failure_rate)
        self.power_kw = power_kw
        self.usage_hours = usage_hours_per_day
        self.electricity_price = 0.65
        self.co2_per_kwh = 0.4

    def energy_consumption(self):
        return self.power_kw * self.usage_hours  # kWh/day

    def operation_time(self):
        return self.usage_hours * 60  # min

    def device_cost(self):
        return 900

    def cost(self):
        return round(self.energy_consumption() * self.electricity_price, 2)

    def co2_emission(self):
        return round(self.energy_consumption() * self.co2_per_kwh, 3)

    def heating_quality(self):
        return 0.75  # przyjemne lokalne ciepło + suszenie ręczników

    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data
    
class FloorHeating(Appliance):
    def __init__(self, area_m2=4.0, power_density_kw_m2=0.12, usage_hours_per_day=5.0,
                 comfort_penalty=0.01, failure_rate=0.02):
        super().__init__("FloorHeating", comfort_penalty, failure_rate)
        self.area = area_m2
        self.power_density = power_density_kw_m2
        self.usage_hours = usage_hours_per_day
        self.electricity_price = 0.65
        self.co2_per_kwh = 0.4

    def energy_consumption(self):
        return self.area * self.power_density * self.usage_hours

    def operation_time(self):
        return self.usage_hours * 60

    def device_cost(self):
        return 2000

    def cost(self):
        return round(self.energy_consumption() * self.electricity_price, 2)

    def co2_emission(self):
        return round(self.energy_consumption() * self.co2_per_kwh, 3)

    def heating_quality(self):
        return 0.95  # super komfort cieplny

    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data
    
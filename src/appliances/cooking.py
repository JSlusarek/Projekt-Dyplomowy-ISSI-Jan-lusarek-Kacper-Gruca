from src.appliances.base import Appliance


class Kettle(Appliance):
    def __init__(self, liters=1.0, comfort_penalty=0.0, failure_rate=0.0):
        super().__init__("Kettle", comfort_penalty=comfort_penalty, failure_rate=failure_rate)
        self.liters = liters

    def energy_consumption(self):
        specific_heat_kj_per_kg_c = 4.186
        temp_rise_c = 80
        efficiency = 0.9
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c
        return energy_kj / 3600 / efficiency

    def operation_time(self):
        power_kw = 2.0
        return (self.energy_consumption() / power_kw) * 60

    def device_cost(self):
        return 300
    

class InductionHob(Appliance):
    def __init__(self, liters=1.0, comfort_penalty=0.0, failure_rate=0.0):
        super().__init__("InductionHob", comfort_penalty=comfort_penalty, failure_rate=failure_rate)
        self.liters = liters

    def energy_consumption(self):
        specific_heat_kj_per_kg_c = 4.186
        temp_rise_c = 80
        efficiency = 0.74
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c
        return energy_kj / 3600 / efficiency

    def operation_time(self):
        power_kw = 1.8
        return (self.energy_consumption() / power_kw) * 60

    def device_cost(self):
        return 2100
    

class GasHob(Appliance):
    def __init__(self, liters=1.0, comfort_penalty=0.0, failure_rate=0.0):
        super().__init__("GasHob", comfort_penalty=comfort_penalty, failure_rate=failure_rate)
        self.liters = liters

    def energy_consumption(self):
        m3_gas = self.liters * 0.015
        return m3_gas * 9.5 / 0.6

    def operation_time(self):
        return 6.0 * self.liters

    def cost(self):
        m3_gas = self.liters * 0.015
        return round(m3_gas * 2.80, 2)

    def device_cost(self):
        return 1500

from src.appliances.base import Appliance


class Shower(Appliance):
    def __init__(self, duration_min=8, flow_rate_lpm=9.0, comfort_penalty=0.02, failure_rate=0.02):
        super().__init__("Shower", comfort_penalty, failure_rate)
        self.duration_min = duration_min
        self.flow_rate_lpm = flow_rate_lpm

    def energy_consumption(self):
        liters = self.flow_rate_lpm * self.duration_min
        specific_heat_kj_per_kg_c = 4.186
        temp_rise_c = 35
        energy_kj = liters * specific_heat_kj_per_kg_c * temp_rise_c
        return energy_kj / 3600

    def operation_time(self):
        return self.duration_min

    def device_cost(self):
        return 2000
    

class Bathtub(Appliance):
    def __init__(self, liters=150, comfort_penalty=0.005, failure_rate=0.03):
        super().__init__("Bathtub", comfort_penalty, failure_rate)
        self.liters = liters

    def energy_consumption(self):
        specific_heat_kj_per_kg_c = 4.186
        temp_rise_c = 35
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c
        return energy_kj / 3600

    def operation_time(self):
        return 15.0

    def device_cost(self):
        return 2500

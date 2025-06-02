from src.appliances.base import Appliance


class Microwave(Appliance):
    def __init__(self, time_minutes=5, comfort_penalty=0.05, failure_rate=0.08, heating_quality=0.4):
        super().__init__("Microwave", comfort_penalty, failure_rate)
        self.time_minutes = time_minutes
        self._heating_quality = heating_quality

    def energy_consumption(self):
        power_kw = 0.9
        return power_kw * (self.time_minutes / 60)

    def operation_time(self):
        return self.time_minutes

    def device_cost(self):
        return 500

    def heating_quality(self):
        return self._heating_quality
    
    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data


class ElectricOven(Appliance):
    def __init__(self, time_minutes=30, comfort_penalty=0.15, failure_rate=0.12, heating_quality=0.9):
        super().__init__("ElectricOven", comfort_penalty, failure_rate)
        self.time_minutes = time_minutes
        self._heating_quality = heating_quality

    def energy_consumption(self):
        power_kw = 2.5
        preheat_minutes = 10
        total_time = self.time_minutes + preheat_minutes
        return power_kw * (total_time / 60)

    def operation_time(self):
        return self.time_minutes + 10

    def device_cost(self):
        return 2000

    def heating_quality(self):
        return self._heating_quality
    
    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data


class AirFryer(Appliance):
    def __init__(self, time_minutes=20, comfort_penalty=0.1, failure_rate=0.1, heating_quality=0.85):
        super().__init__("AirFryer", comfort_penalty, failure_rate)
        self.time_minutes = time_minutes
        self._heating_quality = heating_quality

    def energy_consumption(self):
        power_kw = 1.5
        return power_kw * (self.time_minutes / 60)

    def operation_time(self):
        return self.time_minutes

    def device_cost(self):
        return 800

    def heating_quality(self):
        return self._heating_quality
    
    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data


class GasOven(Appliance):
    def __init__(self, time_minutes=30, comfort_penalty=0.2, failure_rate=0.1, heating_quality=0.88):
        super().__init__("GasOven", comfort_penalty, failure_rate)
        self.time_minutes = time_minutes
        self._heating_quality = heating_quality

    def energy_consumption(self):
        thermal_power_kw = 2.1
        efficiency = 0.6
        preheat_minutes = 8 # czas nagrzewania pieca
        total_minutes = self.time_minutes + preheat_minutes
        energy_input_kwh = thermal_power_kw * (total_minutes / 60) # Czesc energii sie wytrąca
        return energy_input_kwh / efficiency

    def cost(self):
        m3_gas = self.energy_consumption() / 9.5
        return round(m3_gas * 2.80, 2)

    def operation_time(self):
        return self.time_minutes + 10 # czas nagrzewania pieczenia

    def device_cost(self):
        return 1800

    def heating_quality(self):
        return self._heating_quality
    
    def summary(self):
        data = super().summary()
        data["heating_quality"] = self.heating_quality()
        return data
    
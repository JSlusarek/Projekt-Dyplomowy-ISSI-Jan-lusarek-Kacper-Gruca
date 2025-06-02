from src.appliances.base import Appliance


class ElectricHeater(Appliance): 
    def __init__(self, liters=50, comfort_penalty=0.05, failure_rate=0.05): 
        super().__init__("ElectricHeater", comfort_penalty, failure_rate) 
        self.liters = liters 
 
    def energy_consumption(self): 
        specific_heat_kj_per_kg_c = 4.186 
        temp_rise_c = 40 
        efficiency = 1.0 
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c 
        return energy_kj / 3600 / efficiency  
 
    def operation_time(self): 
        power_kw = 2.0 
        return (self.energy_consumption() / power_kw) * 60  

    def device_cost(self): 
        return 1200  

    def heating_quality(self): 
        return 0.4
    
    def cost_per_kwh_heat(self):
        electricity_price = 0.65  # 
        return electricity_price / 1.0

    def summary(self):
        data = super().summary()
        data["co2_per_kwh_heat"] = self.heating_quality()
        data["cost_per_kwh_heat"] = self.cost_per_kwh_heat()
        return data
    

class GasHeater(Appliance): 
    def __init__(self, liters=50, comfort_penalty=0.08, failure_rate=0.07): 
        super().__init__("GasHeater", comfort_penalty, failure_rate) 
        self.liters = liters 
 
    def energy_consumption(self): 
        m3_gas = self.liters * 0.02 
        return m3_gas * 9.5 / 0.9 
 
    def operation_time(self): 
        return 8.0 * (self.liters / 50) 
 
    def cost(self): 
        m3_gas = self.energy_consumption() / 9.5 
        return round(m3_gas * 2.80, 2) 
 
    def co2_emission(self): 
        return round(self.energy_consumption() * 0.19, 3) 
 
    def heat_output(self): 
        return self.energy_consumption() * 0.9 
 
    def device_cost(self): 
        return 1400

    def cost_per_kwh_heat(self):
        return 2.80 / 9.5  
    
    def heating_quality(self): 
        return 0.19  # kg CO₂ / kWh dla spalania gazu ziemnego

    def summary(self):
        data = super().summary()
        data["co2_per_kwh_heat"] = self.heating_quality()
        data["cost_per_kwh_heat"] = self.cost_per_kwh_heat()
        return data


class FlowHeater(Appliance): 
    def __init__(self, liters=50, comfort_penalty=0.04, failure_rate=0.04): 
        super().__init__("FlowHeater", comfort_penalty, failure_rate) 
        self.liters = liters 
 
    def energy_consumption(self): 
        specific_heat_kj_per_kg_c = 4.186 
        temp_rise_c = 40 
        efficiency = 1.0 
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c 
        return energy_kj / 3600 / efficiency 
 
    def operation_time(self): 
        power_kw = 7.0 
        return (self.energy_consumption() / power_kw) * 60 
 
    def device_cost(self): 
        return 1000

    def heating_quality(self): 
        return 0.4  # jak dla prądu w PL

    def cost_per_kwh_heat(self):
        electricity_price = 1.0
        return electricity_price / 1.0

    def summary(self):
        data = super().summary()
        data["co2_per_kwh_heat"] = self.heating_quality()
        data["cost_per_kwh_heat"] = self.cost_per_kwh_heat()
        return data


class HeatPump(Appliance): 
    def __init__(self, liters=50, cop=3.0, comfort_penalty=0.03, failure_rate=0.06): 
        super().__init__("HeatPump", comfort_penalty, failure_rate) 
        self.liters = liters 
        self.cop = cop 
 
    def energy_consumption(self): 
        specific_heat_kj_per_kg_c = 4.186 
        temp_rise_c = 40 
        energy_kj = self.liters * specific_heat_kj_per_kg_c * temp_rise_c 
        return energy_kj / 3600 / self.cop 
 
    def operation_time(self): 
        power_kw = 1.2 
        return (self.energy_consumption() / power_kw) * 60 
 
    def heat_output(self): 
        return self.energy_consumption() * self.cop 
 
    def device_cost(self): 
        return 4500

    def heating_quality(self): 
        return round(0.4 / self.cop, 3)  # redukcja śladu CO₂ dzięki COP

    def cost_per_kwh_heat(self):
        electricity_price = 1.0
        return electricity_price / self.cop

    def summary(self):
        data = super().summary()
        data["co2_per_kwh_heat"] = self.heating_quality()
        data["cost_per_kwh_heat"] = self.cost_per_kwh_heat()
        return data

import pandas as pd 

class Appliance:
    """
    Base class for all appliances.
    It defines the common interface for appliances, including methods to calculate energy consumption,
    operation time, cost, comfort, failure rate, and CO2 emissions.
    Each appliance should implement its own logic where needed.
    """

    def __init__(self, name, comfort_penalty=0.0, failure_rate=0.0):
        self.name = name
        self._comfort_penalty = comfort_penalty
        self._failure_rate = failure_rate

    def energy_consumption(self):
        raise NotImplementedError

    def operation_time(self):
        raise NotImplementedError

    def cost(self, price_per_kwh=0.62):
        """
        Estimate the cost of energy consumed based on a given price per kWh.
        """
        return round(self.energy_consumption() * price_per_kwh, 2)

    def comfort_penalty(self):
        """
        Returns a comfort penalty value (0.0–1.0).
        """
        return self._comfort_penalty

    def failure_rate(self):
        """
        Returns a failure rate value (0.0–1.0).
        """
        return self._failure_rate

    def co2_emission(self, emission_factor=0.4):
        """
        Estimates CO2 emissions in kg using a default emission factor of 0.4 kg/kWh.
        """
        return round(self.energy_consumption() * emission_factor, 3)

    def requires_supervision(self):
        """
        Indicates whether the appliance requires user supervision during operation.
        """
        return False

    def priority(self):
        """
        Priority level of the appliance in optimization systems (0–10).
        """
        return 5

    def device_cost(self):
        """
        Returns the upfront cost of the device in PLN.
        """
        raise NotImplementedError

    def summary(self):
        """
        Returns a dictionary summarizing all key metrics of the appliance.
        """
        return {
            "name": self.name,
            "energy_kwh": round(self.energy_consumption(), 3),
            "cost_pln": self.cost(),
            "time_min": self.operation_time(),
            "comfort_penalty": self.comfort_penalty(),
            "co2_emission_kg": self.co2_emission(),
            "requires_supervision": self.requires_supervision(),
            "priority": self.priority(),
            "device_cost": self.device_cost(),
            "failure_rate": self.failure_rate()
        }


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



######################################## Classes for each home area appliance ########################################
class Kitchen:
    """
    Kitchen class functions as a container for various kitchen appliances.
    """

    @staticmethod
    def compare_water_boiling_devices(liters=1.0):
        """
        Compares kettle, induction hob, and gas hob for boiling a given amount of water.

        Parameters:
            liters (float): Volume of water to boil in liters.

        Returns:
            pd.DataFrame: Summary of each appliance including energy, cost, time, comfort, CO2, etc.
        """
        devices = [
            Kettle(liters, comfort_penalty=0.1, failure_rate=0.6),
            InductionHob(liters, comfort_penalty=0.05, failure_rate=0.2),
            GasHob(liters, comfort_penalty=0.15, failure_rate=0.2)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    
    @staticmethod
    def compare_cooking_devices(time_minutes=30):
        """
        Compares GasHob and InductionHob for cooking tasks (not just boiling water).

        Parameters:
            time_minutes (float): Duration of cooking.

        Returns:
            pd.DataFrame: Summary including energy, cost, comfort, etc.
        """
        # Assume 1.8kW power for induction, 2.0kW equivalent thermal power for gas
        induction = InductionHob(liters=0, comfort_penalty=0.05, failure_rate=0.12)
        gas = GasHob(liters=0, comfort_penalty=0.15, failure_rate=0.1)

        # Override methods to simulate cooking instead of boiling
        induction.energy_consumption = lambda: 1.8 * (time_minutes / 60)
        gas.energy_consumption = lambda: (2.0 * (time_minutes / 60)) / 0.6

        devices = [induction, gas]
        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    
    @staticmethod
    def compare_heating_devices(time_minutes=10):
        """
        Compares food heating devices: microwave, electric oven, air fryer, and gas oven.

        Parameters:
            time_minutes (float): Duration of actual heating (excluding preheating, which is handled internally
                                for relevant appliances).

        Returns:
            pd.DataFrame: Summary table including key metrics for each device such as energy consumption (kWh),
                        cost (PLN), operation time (minutes), comfort penalty, CO2 emissions, heating quality,
                        normalized comfort and failure rates, and more.
        """
        devices = [
            Microwave(time_minutes=time_minutes, comfort_penalty=0.05, failure_rate=0.08, heating_quality=0.4),
            ElectricOven(time_minutes=time_minutes, comfort_penalty=0.15, failure_rate=0.12, heating_quality=0.7),
            AirFryer(time_minutes=time_minutes, comfort_penalty=0.1, failure_rate=0.1, heating_quality=0.7),
            GasOven(time_minutes=time_minutes, comfort_penalty=0.2, failure_rate=0.1, heating_quality=0.9)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    
    @staticmethod
    def compare_coffee_devices(cups=1):
        """
        Compares coffee-making appliances: electric moka pot and coffee machine.

        Parameters:
            cups (int): Number of coffee cups to prepare.

        Returns:
            pd.DataFrame: Summary of energy use, cost, time, comfort, coffee taste, etc.
        """
        devices = [
            ElectricMokaPot(cups=cups, comfort_penalty=0.1, failure_rate=0.08, coffee_taste=0.78),
            CoffeeMachine(cups=cups, comfort_penalty=0.05, failure_rate=0.05, coffee_taste=0.9)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    
    @staticmethod
    def compare_multicookers(recipe_complexity=1.0):
        """
        Compares smart cooking appliances like Thermomix TM6 and Bosch Cookit.

        Parameters:
            recipe_complexity (float): 1.0 is standard; higher = longer/more energy-intensive recipes.

        Returns:
            pd.DataFrame: Summary of energy use, cost, cooking quality, etc.
        """
        devices = [
            ThermomixTM6(recipe_complexity=recipe_complexity),
            BoschCookit(recipe_complexity=recipe_complexity)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)


class Bathroom:
    @staticmethod
    def compare_water_heaters(liters=50):
        """
        Compares different water heating devices: Electric Heater, Gas Heater, Flow Heater, and Heat Pump.
        Parameters:
            liters (float): Volume of water to heat in liters.
        """
        devices = [
            ElectricHeater(liters=liters),
            GasHeater(liters=liters),
            FlowHeater(liters=liters),
            HeatPump(liters=liters)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    

    @staticmethod
    def compare_bathing_options():
        devices = [
            Shower(duration_min=8),
            Bathtub(liters=150)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)
    

    @staticmethod
    def compare_bathroom_heating():

        devices = [
            LadderHeater(),
            FloorHeating()
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3)
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3)
            results.append(summary)

        return pd.DataFrame(results)


class Room:
    
    @staticmethod
    def compare_workstations():
        devices = [
            DesktopComputer(),
            LaptopWithMonitor()
        ]

        total_comfort = sum(d.comfort_penalty() for d in devices)
        total_failure = sum(d.failure_rate() for d in devices)

        results = []
        for d in devices:
            summary = d.summary()
            summary["normalized_comfort"] = round(d.comfort_penalty() / total_comfort, 3)
            summary["normalized_failure_rate"] = round(d.failure_rate() / total_failure, 3)
            results.append(summary)

        return pd.DataFrame(results)


    @staticmethod
    def compare_cooling_devices(duration_min=60):
        devices = [
            AirConditioner(duration_min=duration_min),
            Fan(duration_min=duration_min)
        ]

        total_comfort = sum(dev.comfort_penalty() for dev in devices)
        total_failure = sum(dev.failure_rate() for dev in devices)

        results = []
        for dev in devices:
            summary = dev.summary()
            summary["normalized_comfort"] = round(dev.comfort_penalty() / total_comfort, 3) if total_comfort > 0 else 0
            summary["normalized_failure_rate"] = round(dev.failure_rate() / total_failure, 3) if total_failure > 0 else 0
            results.append(summary)

        return pd.DataFrame(results)











################################### Optimization function to find the best device##################### 

def find_optimal_device(df, weights):
    """
    Finds the optimal device based on weighted scores of different criteria.

    Parameters:
        df (pd.DataFrame): The DataFrame from compare_water_boiling_devices.
        weights (dict): Mapping from column names to their respective weights. Weights must sum to 1.

    Returns:
        pd.DataFrame: Original DataFrame with an added 'score' column, sorted descending by score.
    """
    if not abs(sum(abs(w) for w in weights.values()) - 1.0) < 1e-6:
        raise ValueError("Absolute sum of weights must be 1.0")


    df = df.copy()
    df["score"] = 0.0
    for col, weight in weights.items():
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max > col_min:
            normalized = (df[col] - col_min) / (col_max - col_min)
        else:
            normalized = 0
        df["score"] += normalized * weight
    return df.sort_values(by="score", ascending=False).reset_index(drop=True)

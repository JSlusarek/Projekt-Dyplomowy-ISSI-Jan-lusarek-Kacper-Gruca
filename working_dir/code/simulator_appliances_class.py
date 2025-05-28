import pandas as pd


class Appliance:

    """
    Base class for all appliances. 
    It defines the common interface for appliances, including methods to calculate energy consumption,
    operation time, and cost.
    Each appliance should implement its own energy consumption and operation time logic.
    """

    def __init__(self, name):
        self.name = name

    def energy_consumption(self):
        raise NotImplementedError

    def operation_time(self):
        raise NotImplementedError

    def cost(self, price_per_kwh=0.62): # Poniżej podana cena 1 kWh energii elektrycznej w Polsce na początku 2025 roku
    # https://corab.pl/aktualnosci/ile-kosztuje-1-kwh-energii-elektrycznej-w-2025-roku-z-czego-wynika-cena#:~:text=Na%20początku%202025%20roku%20ceny%20energii%20elektrycznej,(0%2C6212%20zł%20brutto%20z%20VAT%20i%20akcyzą).
        return round(self.energy_consumption() * price_per_kwh, 2)


class Dishwasher(Appliance):
    """
    Dishwasher class with different profiles for operation.
    Each profile has a specific time and energy consumption.
    """

    profiles = {
        "eco": {"time": 180, "energy": 0.8},
        "normal": {"time": 120, "energy": 1.0},
        "quick": {"time": 60, "energy": 1.2},
        "intensive": {"time": 45, "energy": 1.4}
    }

    def __init__(self, profile):
        super().__init__("Dishwasher")
        self.profile = profile

    def energy_consumption(self):
        return self.profiles[self.profile]["energy"]

    def operation_time(self):
        return self.profiles[self.profile]["time"]



class WashingMachine(Appliance):
    """
    WashingMachine class with different profiles for operation.
    Each profile has a specific time and energy consumption.
    """

    profiles = {
        "eco": {"time": 150, "energy": 0.7},
        "normal": {"time": 90, "energy": 1.0},
        "quick": {"time": 45, "energy": 1.3}
    }

    def __init__(self, profile):
        super().__init__("WashingMachine")
        self.profile = profile

    def energy_consumption(self):
        return self.profiles[self.profile]["energy"]

    def operation_time(self):
        return self.profiles[self.profile]["time"]


class Kettle(Appliance):

    """
    Kettle class to simulate the energy consumption and operation time of a kettle.
    It calculates the energy needed to heat water based on its volume and temperature rise.
    """
    def __init__(self, liters=1.0):
        super().__init__("Kettle")
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



class InductionHob(Appliance):

    """
    InductionHob class to simulate the energy consumption and operation time of an induction hob.
    It calculates the energy needed to heat water based on its volume and temperature rise.
    """

    def __init__(self, liters=1.0):
        super().__init__("InductionHob")
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



class GasHob(Appliance):

    """ 
    GasHob class to simulate the energy consumption and operation time of a gas hob.
    It calculates the energy needed to heat water based on its volume and gas consumption.
    """

    def __init__(self, liters=1.0):
        super().__init__("GasHob")
        self.liters = liters

    def energy_consumption(self):
        m3_gas = self.liters * 0.015
        return m3_gas * 9.5 / 0.6

    def operation_time(self):
        return 6.0 * self.liters

    def cost(self):
        m3_gas = self.liters * 0.015
        return round(m3_gas * 2.80, 2)



def check_network_load(devices, max_kw=3.0):
    """
    Check if the total energy consumption of devices exceeds the maximum allowed power in kW.
    """

    return sum([dev.energy_consumption() / (dev.operation_time() / 60) for dev in devices]) <= max_kw



def summarize_device_stats(**kwargs):
    """
    Creates instances of selected appliances with provided parameters and computes their energy and cost.

    Parameters (as kwargs):
        kettle: float - liters
        dishwasher: str - profile
        washing_machine: str - profile
        induction: float - liters
        gas: float - liters

    Returns:
        pd.DataFrame: Table with columns 'Device', 'Energy (kWh)', and 'Cost (PLN)'
    """

    devices = []

    if "kettle" in kwargs:
        devices.append(Kettle(kwargs["kettle"]))
    if "dishwasher" in kwargs:
        devices.append(Dishwasher(kwargs["dishwasher"]))
    if "washing_machine" in kwargs:
        devices.append(WashingMachine(kwargs["washing_machine"]))
    if "induction" in kwargs:
        devices.append(InductionHob(kwargs["induction"]))
    if "gas" in kwargs:
        devices.append(GasHob(kwargs["gas"]))

    device_stats = [
        (dev.name, round(dev.energy_consumption(), 3), dev.cost())
        for dev in devices
    ]

    return pd.DataFrame(device_stats, columns=["Device", "Energy (kWh)", "Cost (PLN)"])

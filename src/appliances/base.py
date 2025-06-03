from abc import ABC, abstractmethod

class Appliance(ABC):
    """
    Abstract base class for all household appliances.

    This class defines the common interface and core functionality shared by all appliances,
    including methods for estimating energy consumption, runtime, cost, CO₂ emissions, comfort impact, etc.

    Subclasses must implement device-specific logic.
    """

    def __init__(self, name, comfort_penalty=0.0, failure_rate=0.0):
        """
        Initialize the appliance.

        Args:
            name (str): The name of the appliance.
            comfort_penalty (float): Discomfort level from using the device (0.0 to 1.0).
            failure_rate (float): Probability of failure or unreliability (0.0 to 1.0).
        """
        self.name = name
        self._comfort_penalty = comfort_penalty
        self._failure_rate = failure_rate

    @abstractmethod
    def energy_consumption(self):
        """
        Returns:
            float: Estimated energy consumption in kilowatt-hours (kWh).
        """
        pass

    @abstractmethod
    def operation_time(self):
        """
        Returns:
            float: Estimated operation time in minutes.
        """
        pass

    @abstractmethod
    def device_cost(self):
        """
        Returns:
            float: The upfront cost of the appliance in PLN.
        """
        pass

    def cost(self, price_per_kwh=0.62):
        """
        Estimate the cost of energy consumption.

        Args:
            price_per_kwh (float): Price of electricity per kWh.

        Returns:
            float: Total cost in PLN, rounded to 2 decimal places.
        """
        return round(self.energy_consumption() * price_per_kwh, 2)

    def comfort_penalty(self):
        """
        Returns:
            float: User comfort penalty from using the appliance (0.0 to 1.0).
        """
        return self._comfort_penalty

    def failure_rate(self):
        """
        Returns:
            float: Probability of device failure or inconvenience (0.0 to 1.0).
        """
        return self._failure_rate

    def co2_emission(self, emission_factor=0.4):
        """
        Estimate the CO2 emissions based on energy usage.

        Args:
            emission_factor (float): CO2 emission factor (kg per kWh), default is 0.4.

        Returns:
            float: Estimated CO2 emissions in kilograms.
        """
        return round(self.energy_consumption() * emission_factor, 3)
    
    def summary(self):
        """
        Generate a summary of the appliance's key performance metrics.

        Returns:
            dict: Dictionary containing energy, cost, comfort, emissions, and other relevant data.
        """
        return {
            "name": self.name,
            "energy_kwh": round(self.energy_consumption(), 3),
            "cost_pln": self.cost(),
            "time_min": self.operation_time(),
            "comfort_penalty": self.comfort_penalty(),
            "co2_emission_kg": self.co2_emission(),
            "device_cost": self.device_cost(),
            "failure_rate": self.failure_rate()
        }

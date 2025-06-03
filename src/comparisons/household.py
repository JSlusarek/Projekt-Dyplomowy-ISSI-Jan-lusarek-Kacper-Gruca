# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join("../../")))

import pandas as pd
from src.appliances.cooking import Kettle, InductionHob, GasHob
from src.appliances.ovens import Microwave, ElectricOven, AirFryer, GasOven
from src.appliances.coffee import ElectricMokaPot, CoffeeMachine
from src.appliances.multicookers import ThermomixTM6, BoschCookit
from src.appliances.heating import ElectricHeater, GasHeater, FlowHeater, HeatPump
from src.appliances.bathing import Shower, Bathtub
from src.appliances.bathroom_heating import LadderHeater, FloorHeating
from src.appliances.workstations import DesktopComputer, LaptopWithMonitor
from src.appliances.cooling import AirConditioner, Fan


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
        gas.operation_time= lambda: time_minutes
        gas.cost = lambda: round(gas.energy_consumption() * 2.80 / 9.5, 2)  # m3 gas cost

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

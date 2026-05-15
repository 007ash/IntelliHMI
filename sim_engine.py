import random
import time
from datetime import datetime

class SimulationEngine:
    def __init__(self):
        self.tick = 0
        self.base_temp = 65.0 # Celsius
        self.base_pressure = 120.0 # PSI
        self.base_vibration = 2.5 # mm/s
        self.base_gas = 0.0 # ppm
        self.base_power = 450.0 # kW
        
        self.scenario_active = True

    def get_sensor_data(self):
        """Generates the next tick of sensor data, incorporating the demo scenario."""
        self.tick += 1
        
        # Base realistic fluctuations
        temp = self.base_temp + random.uniform(-2, 2)
        pressure = self.base_pressure + random.uniform(-5, 5)
        vibration = self.base_vibration + random.uniform(-0.5, 0.5)
        gas = self.base_gas + random.uniform(0, 0.5) if self.base_gas > 0 else random.uniform(0, 0.1)
        power = self.base_power + random.uniform(-10, 10)

        # Demo Scenario Logic
        # Tick 1-10: Normal
        # Tick 11-20: Temp starts rising
        # Tick 21-30: Temp high + Vibration spikes
        # Tick 31-40: Pressure instability
        # Tick 41+: Gas leakage risk appears, everything critical
        
        # Loop scenario every 60 ticks for demo purposes
        cycle_tick = self.tick % 60
        
        if self.scenario_active:
            if cycle_tick > 10:
                # Overheating
                temp += (cycle_tick - 10) * 1.5
                power += (cycle_tick - 10) * 2.0
            
            if cycle_tick > 20:
                # Vibration spikes
                vibration += (cycle_tick - 20) * 0.4
            
            if cycle_tick > 30:
                # Pressure instability
                pressure += random.choice([-1, 1]) * (cycle_tick - 30) * 1.2
            
            if cycle_tick > 40:
                # Gas leak risk
                gas += (cycle_tick - 40) * 0.8
                
        # Format the data
        data = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "tick": self.tick,
            "cycle_tick": cycle_tick,
            "sensors": {
                "temperature": {"value": round(temp, 1), "unit": "°C"},
                "pressure": {"value": round(pressure, 1), "unit": "PSI"},
                "vibration": {"value": round(vibration, 2), "unit": "mm/s"},
                "gas_leakage": {"value": round(gas, 1), "unit": "ppm"},
                "power_consumption": {"value": round(power, 0), "unit": "kW"}
            }
        }
        return data

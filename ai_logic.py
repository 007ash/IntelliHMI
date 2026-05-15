class AIEngine:
    def __init__(self):
        # Define thresholds: (medium, high, critical)
        self.thresholds = {
            "temperature": (75.0, 85.0, 95.0),
            "pressure": (130.0, 140.0, 150.0),
            "vibration": (3.5, 4.5, 6.0),
            "gas_leakage": (5.0, 10.0, 15.0),
            "power_consumption": (500.0, 550.0, 600.0)
        }

    def evaluate_alarms(self, sensor_data):
        alarms = []
        for sensor, data in sensor_data["sensors"].items():
            val = data["value"]
            med, high, crit = self.thresholds[sensor]
            
            severity = "Normal"
            score = 0
            if val >= crit:
                severity = "Critical"
                score = 100
            elif val >= high:
                severity = "High"
                score = 75
            elif val >= med:
                severity = "Medium"
                score = 50
                
            if severity != "Normal":
                alarms.append({
                    "sensor": sensor.replace("_", " ").title(),
                    "value": val,
                    "unit": data["unit"],
                    "severity": severity,
                    "score": score
                })
        
        # Sort by score descending
        return sorted(alarms, key=lambda x: x["score"], reverse=True)

    def group_incidents(self, alarms):
        clusters = []
        sensor_names = [a["sensor"].lower() for a in alarms]
        
        # Rule 1: Motor Failure
        if "temperature" in sensor_names and "vibration" in sensor_names:
            clusters.append({
                "name": "Possible Motor Failure Cluster",
                "severity": "Critical" if any(a["severity"] == "Critical" for a in alarms if a["sensor"].lower() in ["temperature", "vibration"]) else "High",
                "related_sensors": ["Temperature", "Vibration"]
            })
            
        # Rule 2: Pipeline Instability
        if "pressure" in sensor_names and "vibration" in sensor_names:
            clusters.append({
                "name": "Pipeline Instability Detected",
                "severity": "High",
                "related_sensors": ["Pressure", "Vibration"]
            })
            
        # Rule 3: Severe Hazard
        if "gas leakage" in sensor_names:
            clusters.append({
                "name": "Hazardous Gas Leak Warning",
                "severity": "Critical",
                "related_sensors": ["Gas Leakage"]
            })
            
        return clusters

    def generate_root_cause(self, clusters):
        insights = []
        for cluster in clusters:
            if "Motor" in cluster["name"]:
                insights.append({
                    "cause": "Pump overheating likely caused by abnormal vibration and cooling inefficiency detected over the last 10 minutes.",
                    "confidence": "92%",
                    "action": "Initiate emergency cooling protocol and schedule maintenance for primary motor bearing."
                })
            elif "Pipeline" in cluster["name"]:
                insights.append({
                    "cause": "Pressure fluctuations are correlating with physical pipe vibrations, suggesting a potential valve malfunction or blockage.",
                    "confidence": "85%",
                    "action": "Isolate the affected pipeline segment and inspect safety release valves."
                })
            elif "Gas" in cluster["name"]:
                insights.append({
                    "cause": "Uncontained gas buildup detected. Sensors indicate a seal failure in Sector 4.",
                    "confidence": "98%",
                    "action": "EVACUATE SECTOR 4 IMMEDIATELY. Trigger automated ventilation sequence."
                })
        
        if not insights:
            insights.append({
                "cause": "All systems operating within acceptable parameters. Minor fluctuations are being monitored.",
                "confidence": "99%",
                "action": "No action required at this time."
            })
            
        return insights

    def predict_failure(self, alarms, cycle_tick):
        # Base probability is low
        prob = 5.0
        
        # Increase based on alarms
        for alarm in alarms:
            if alarm["severity"] == "Critical":
                prob += 25.0
            elif alarm["severity"] == "High":
                prob += 10.0
            elif alarm["severity"] == "Medium":
                prob += 5.0
                
        # Time-based urgency (simulating an escalating situation in the demo)
        if cycle_tick > 45:
            prob += 30.0
            
        # Cap at 99%
        prob = min(prob, 99.9)
        
        time_to_failure = "N/A"
        if prob > 80:
            time_to_failure = "10 mins"
        elif prob > 50:
            time_to_failure = "45 mins"
        elif prob > 20:
            time_to_failure = "2 hours"
            
        return round(prob, 1), time_to_failure

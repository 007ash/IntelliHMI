# IntelliHMI ⚡

**IntelliHMI** is a next-generation adaptive Human-Machine Interface (HMI) dashboard prototype designed for industrial operators. Built with Streamlit, it reduces alarm fatigue, prioritizes critical alerts, predicts failures, and provides AI-assisted operational insights.

This project was built to demonstrate how AI and modern UX design can transform industrial control systems into intelligent, predictive assistants.

## 🌟 Key Features

*   **Real-Time Sensor Simulation:** Simulates live industrial data (Temperature, Pressure, Vibration, Gas Leakage, Power Consumption) with realistic fluctuations and anomalies.
*   **AI-Powered Alarm Prioritization:** Intelligently scores and classifies alerts (Critical, High, Medium, Low) to reduce cognitive overload for operators.
*   **Smart Incident Grouping:** Correlates multiple sensor spikes (e.g., High Temperature + Vibration) into unified incident clusters (e.g., "Motor Failure Risk").
*   **AI Root Cause Assistant:** Translates raw data into plain-language actionable insights and suggested mitigation steps.
*   **Predictive Warning System:** Calculates real-time failure probabilities and estimates time-to-failure based on active threats.
*   **Role-Based Views:** Dynamic interface offering tailored information for **Operators** (actionable insights), **Engineers** (telemetry charts), and **Managers** (high-level health scores).
*   **Modern "Glassmorphism" UI:** Premium, dark-mode design mimicking modern SaaS platforms, creating a stark contrast to traditional clunky HMIs.

## 📂 Project Structure

*   `app.py`: The main Streamlit dashboard application orchestrating the UI layout and navigation.
*   `sim_engine.py`: Contains the data generation logic and the built-in "Demo Scenario" state machine.
*   `ai_logic.py`: The intelligent backend evaluating alarms, grouping incidents, generating text insights, and predicting failures.
*   `ui_components.py`: Modular Streamlit/HTML helper functions for rendering the custom glassmorphism cards and Plotly charts.
*   `assets/style.css`: Custom styling injected into the Streamlit app to enforce the premium dark-mode aesthetic.
*   `requirements.txt`: List of Python dependencies.

## ⚙️ Installation

1. Clone or download this repository.
2. Ensure you have Python installed.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Demo

To launch the IntelliHMI dashboard, run the following command in your terminal:

```bash
python -m streamlit run app.py
```

The application will start a local server and provide a URL (typically `http://localhost:8501`) that you can open in your web browser.

### 💡 Demo Scenario Tip
To demonstrate the full capability of the AI during a presentation:
1. Ensure the **"Trigger Demo Scenario"** toggle is active in the sidebar.
2. Watch the live data feed over the span of a minute. The system will progressively introduce an anomaly (e.g., rising temperature and vibration).
3. Observe how the system automatically groups these alerts into a single incident cluster and generates a root cause analysis!

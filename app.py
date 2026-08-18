import streamlit as st
import pandas as pd
import time
import os

from sim_engine import SimulationEngine
from ai_logic import AIEngine
from ui_components import render_metric_card, render_ai_insight, render_sensor_chart, render_risk_gauge

st.set_page_config(page_title="IntelliHMI", page_icon="⚡", layout="wide")

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

if 'sim_engine' not in st.session_state:
    st.session_state.sim_engine = SimulationEngine()
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = AIEngine()
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['time', 'temperature', 'pressure', 'vibration', 'gas_leakage', 'power_consumption'])
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

with st.sidebar:
    st.markdown("<div style='font-size: 2rem; font-weight: 700; color: #f8fafc; margin-bottom: 20px;'>⚡ IntelliHMI</div>", unsafe_allow_html=True)
    
    role = st.selectbox("Select Role", ["Operator", "Engineer", "Manager"])
    
    st.markdown("---")
    st.markdown("<div class='section-header'>Simulation Controls</div>", unsafe_allow_html=True)
    
    st.session_state.auto_refresh = st.toggle("Live Data Feed", value=st.session_state.auto_refresh)
    st.session_state.sim_engine.scenario_active = st.toggle("Trigger Demo Scenario", value=st.session_state.sim_engine.scenario_active)
    
    if st.button("Reset Simulation"):
        st.session_state.sim_engine = SimulationEngine()
        st.session_state.history = pd.DataFrame(columns=['time', 'temperature', 'pressure', 'vibration', 'gas_leakage', 'power_consumption'])
        st.rerun()

data = st.session_state.sim_engine.get_sensor_data()

new_row = {
    'time': data['timestamp'],
    'temperature': data['sensors']['temperature']['value'],
    'pressure': data['sensors']['pressure']['value'],
    'vibration': data['sensors']['vibration']['value'],
    'gas_leakage': data['sensors']['gas_leakage']['value'],
    'power_consumption': data['sensors']['power_consumption']['value']
}
st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)
if len(st.session_state.history) > 30: # Keep last 30 ticks
    st.session_state.history = st.session_state.history.tail(30)

alarms = st.session_state.ai_engine.evaluate_alarms(data)
clusters = st.session_state.ai_engine.group_incidents(alarms)
insights = st.session_state.ai_engine.generate_root_cause(clusters)
fail_prob, fail_time = st.session_state.ai_engine.predict_failure(alarms, data['cycle_tick'])

st.markdown("<div class='title-main'>IntelliHMI Global Overview</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>Real-time Operations Dashboard • {data['timestamp']}</div>", unsafe_allow_html=True)

# Common Top Row (Metrics)
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    v = data['sensors']['temperature']
    sev = next((a['severity'] for a in alarms if a['sensor'].lower() == 'temperature'), 'Normal')
    render_metric_card("Temperature", v['value'], v['unit'], sev)
with col2:
    v = data['sensors']['pressure']
    sev = next((a['severity'] for a in alarms if a['sensor'].lower() == 'pressure'), 'Normal')
    render_metric_card("Pressure", v['value'], v['unit'], sev)
with col3:
    v = data['sensors']['vibration']
    sev = next((a['severity'] for a in alarms if a['sensor'].lower() == 'vibration'), 'Normal')
    render_metric_card("Vibration", v['value'], v['unit'], sev)
with col4:
    v = data['sensors']['gas_leakage']
    sev = next((a['severity'] for a in alarms if a['sensor'].lower() == 'gas leakage'), 'Normal')
    render_metric_card("Gas Leakage", v['value'], v['unit'], sev)
with col5:
    v = data['sensors']['power_consumption']
    sev = next((a['severity'] for a in alarms if a['sensor'].lower() == 'power consumption'), 'Normal')
    render_metric_card("Power", v['value'], v['unit'], sev)

st.markdown("---")

if role == "Operator":
    colA, colB = st.columns([2, 1])
    
    with colA:
        st.markdown("<div class='section-header'>AI Root Cause & Recommended Actions</div>", unsafe_allow_html=True)
        for insight in insights:
            render_ai_insight(insight)
            
        if clusters:
            st.markdown("<div class='section-header' style='margin-top:20px;'>Incident Clusters</div>", unsafe_allow_html=True)
            for c in clusters:
                st.error(f"⚠️ **{c['name']}** (Severity: {c['severity']}) - Correlated Sensors: {', '.join(c['related_sensors'])}")
        elif alarms:
            st.warning("⚠️ Minor isolated alarms active. Monitoring...")
        else:
            st.success("✅ All systems operating normally. No active clusters.")
            
    with colB:
        st.markdown("<div class='section-header'>Failure Prediction</div>", unsafe_allow_html=True)
        render_risk_gauge(fail_prob)
        if fail_time != "N/A":
            st.markdown(f"<div style='text-align:center; color:#ef4444; font-weight:bold;'>Est. Time to Failure: {fail_time}</div>", unsafe_allow_html=True)

elif role == "Engineer":
    st.markdown("<div class='section-header'>Live Sensor Telemetry</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        render_sensor_chart(st.session_state.history, 'temperature', 'Temperature History', color='#ef4444')
        render_sensor_chart(st.session_state.history, 'vibration', 'Vibration History', color='#f97316')
    with c2:
        render_sensor_chart(st.session_state.history, 'pressure', 'Pressure History', color='#38bdf8')
        render_sensor_chart(st.session_state.history, 'gas_leakage', 'Gas Leakage History', color='#10b981')

elif role == "Manager":
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown("<div class='section-header'>System Health</div>", unsafe_allow_html=True)
        render_risk_gauge(100 - fail_prob) # Show health instead of failure risk
        st.markdown("<div style='text-align:center; color:#94a3b8;'>Overall System Health Score</div>", unsafe_allow_html=True)
    with colB:
        st.markdown("<div class='section-header'>Active Threats</div>", unsafe_allow_html=True)
        st.metric("Critical Alerts", len([a for a in alarms if a['severity'] == 'Critical']))
        st.metric("Incident Clusters", len(clusters))
    with colC:
        st.markdown("<div class='section-header'>Efficiency Metrics</div>", unsafe_allow_html=True)
        st.metric("Average Power Usage", f"{data['sensors']['power_consumption']['value']} kW", delta="-12 kW (last hour)", delta_color="inverse")
        st.metric("Uptime", "99.98%", delta="0.01%")

# Trigger next refresh
if st.session_state.auto_refresh:
    time.sleep(2)
    st.rerun()

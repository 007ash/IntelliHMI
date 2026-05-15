import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_metric_card(title, value, unit, severity="Normal"):
    # Map severity to CSS class
    severity_class = f"alert-{severity.lower()}" if severity != "Normal" else ""
    badge_class = f"badge-{severity.lower()}" if severity != "Normal" else ""
    
    html = f'<div class="glass-card {severity_class}"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;"><span style="color: #94a3b8; font-weight: 600; font-size: 0.9rem;">{title.upper()}</span>' + (f'<span class="alert-badge {badge_class}">{severity}</span>' if severity != "Normal" else '') + f'</div><div style="font-size: 2rem; font-weight: 700; color: #f8fafc;">{value} <span style="font-size: 1rem; color: #cbd5e1; font-weight: 400;">{unit}</span></div></div>'
    st.markdown(html, unsafe_allow_html=True)

def render_ai_insight(insight):
    html = f'<div class="ai-insight" style="margin-bottom: 15px;"><div class="ai-icon">🧠</div><div class="ai-text"><div><strong>Probable Cause:</strong> {insight["cause"]}</div><div style="margin-top: 8px;"><strong>Suggested Action:</strong> <span class="ai-highlight">{insight["action"]}</span></div><div style="margin-top: 8px; font-size: 0.8rem; color: #64748b;">Confidence Score: {insight["confidence"]}</div></div></div>'
    st.markdown(html, unsafe_allow_html=True)

def render_sensor_chart(history_df, sensor_key, title, color="#38bdf8"):
    # history_df should have 'time' and sensor_key columns
    if history_df.empty:
        st.warning("Waiting for data...")
        return
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history_df['time'], 
        y=history_df[sensor_key],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)"
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#e2e8f0', size=14)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0),
        height=200,
        xaxis=dict(showgrid=False, color='#64748b', showticklabels=False), # Hide x-axis labels for clean look
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', color='#64748b')
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def render_risk_gauge(probability):
    color = "#10b981" # Green
    if probability > 75:
        color = "#ef4444" # Red
    elif probability > 40:
        color = "#f97316" # Orange
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability,
        number = {'suffix': "%", 'font': {'color': '#f8fafc'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(16, 185, 129, 0.1)'},
                {'range': [40, 75], 'color': 'rgba(249, 115, 22, 0.1)'},
                {'range': [75, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=250,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

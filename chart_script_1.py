import plotly.graph_objects as go
import pandas as pd

# Data for the chart
data = [
    {"metric": "FPS", "value": 30, "unit": "fps", "category": "Performance"},
    {"metric": "Latency", "value": 45, "unit": "ms", "category": "Performance"}, 
    {"metric": "Accuracy", "value": 95, "unit": "%", "category": "Performance"},
    {"metric": "CPU Usage", "value": 15, "unit": "%", "category": "Resource"},
    {"metric": "Memory Usage", "value": 180, "unit": "MB", "category": "Resource"},
    {"metric": "Python Exec", "value": 150, "unit": "MB", "category": "Deployment"},
    {"metric": "Electron Exec", "value": 200, "unit": "MB", "category": "Deployment"}
]

df = pd.DataFrame(data)

# Brand colors in order
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C', '#964325']

# Create horizontal bar chart
fig = go.Figure()

for i, row in df.iterrows():
    fig.add_trace(go.Bar(
        y=[row['metric']],
        x=[row['value']],
        orientation='h',
        name=row['metric'],
        marker_color=colors[i % len(colors)],
        text=[f"{row['value']}{row['unit']}"],
        textposition='outside',
        cliponaxis=False,
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title="CamMouse Performance Metrics",
    xaxis_title="Value",
    yaxis_title="Metric"
)

# Save the chart
fig.write_image("cammouse_metrics.png")
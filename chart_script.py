import pandas as pd
import plotly.graph_objects as go

# Load the data
data = [
    {
        "layer": "Input Layer",
        "component": "Camera/Webcam",
        "description": "Video capture at 30 FPS",
        "technology": "OpenCV VideoCapture",
        "performance": "640x480 @ 30fps"
    },
    {
        "layer": "Processing Layer", 
        "component": "MediaPipe Hands",
        "description": "21 landmark detection",
        "technology": "Google MediaPipe",
        "performance": "95% accuracy"
    },
    {
        "layer": "Processing Layer",
        "component": "Gesture Recognition",
        "description": "Pinch detection & cursor tracking", 
        "technology": "Euclidean distance calculation",
        "performance": "< 50ms latency"
    },
    {
        "layer": "Control Layer",
        "component": "PyAutoGUI",
        "description": "System cursor control",
        "technology": "OS-level mouse control",
        "performance": "Global desktop access"
    },
    {
        "layer": "Output Layer",
        "component": "Desktop Interaction",
        "description": "Mouse movement & clicks",
        "technology": "Cross-platform support",
        "performance": "Real-time response"
    },
    {
        "layer": "Deployment",
        "component": "Python Executable",
        "description": "PyInstaller packaging",
        "technology": "Standalone .exe",
        "performance": "~150MB size"
    },
    {
        "layer": "Deployment", 
        "component": "Electron App",
        "description": "Cross-platform desktop",
        "technology": "Node.js + Electron",
        "performance": "~200MB size"
    }
]

df = pd.DataFrame(data)

# Define colors
colors = ['#1FB8CD', '#FFC185', '#ECEBD5', '#5D878F', '#D2BA4C', '#B4413C', '#964325']

# Create coordinates for each component with performance metrics
components = [
    {'x': 2, 'y': 6, 'component': 'Camera', 'layer': 'Input', 'perf': '30fps', 'tech': 'OpenCV', 'index': 0},
    {'x': 1, 'y': 4.5, 'component': 'MediaPipe', 'layer': 'Processing', 'perf': '95% accuracy', 'tech': 'Hand Detection', 'index': 1},
    {'x': 3, 'y': 4.5, 'component': 'Gesture Recog', 'layer': 'Processing', 'perf': '<50ms latency', 'tech': 'Euclidean Calc', 'index': 2},
    {'x': 2, 'y': 3, 'component': 'PyAutoGUI', 'layer': 'Control', 'perf': 'Global access', 'tech': 'OS Control', 'index': 3},
    {'x': 2, 'y': 1.5, 'component': 'Desktop UI', 'layer': 'Output', 'perf': 'Real-time', 'tech': 'Cross-platform', 'index': 4},
    {'x': 1, 'y': 0, 'component': 'Python EXE', 'layer': 'Deploy', 'perf': '150MB', 'tech': 'PyInstaller', 'index': 5},
    {'x': 3, 'y': 0, 'component': 'Electron App', 'layer': 'Deploy', 'perf': '200MB', 'tech': 'Node.js', 'index': 6}
]

# Create the figure
fig = go.Figure()

# Add flow lines with arrows
flow_connections = [
    (2, 6, 1, 4.5),    # Camera to MediaPipe
    (2, 6, 3, 4.5),    # Camera to Gesture Recognition
    (1, 4.5, 2, 3),    # MediaPipe to PyAutoGUI
    (3, 4.5, 2, 3),    # Gesture Recognition to PyAutoGUI
    (2, 3, 2, 1.5),    # PyAutoGUI to Desktop
    (2, 1.5, 1, 0),    # Desktop to Python EXE
    (2, 1.5, 3, 0),    # Desktop to Electron App
]

# Add arrow lines
for x1, y1, x2, y2 in flow_connections:
    # Calculate arrow direction
    dx = x2 - x1
    dy = y2 - y1
    
    # Add line
    fig.add_trace(go.Scatter(
        x=[x1, x2],
        y=[y1, y2],
        mode='lines',
        line=dict(color='#13343B', width=3),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrowhead using shapes
    fig.add_shape(
        type="line",
        x0=x1, y0=y1, x1=x2, y1=y2,
        line=dict(color='#13343B', width=3),
        layer="below"
    )

# Add component nodes
for comp in components:
    # Main component marker
    fig.add_trace(go.Scatter(
        x=[comp['x']],
        y=[comp['y']],
        mode='markers+text',
        marker=dict(
            size=70,
            color=colors[comp['index'] % len(colors)],
            line=dict(width=3, color='white')
        ),
        text=comp['component'],
        textposition='middle center',
        textfont=dict(size=8, color='white', family='Arial Black'),
        hovertemplate=f"<b>{comp['component']}</b><br>" +
                     f"Tech: {comp['tech']}<br>" +
                     f"Perf: {comp['perf']}<br>" +
                     "<extra></extra>",
        showlegend=False
    ))
    
    # Add performance metrics below each component
    fig.add_trace(go.Scatter(
        x=[comp['x']],
        y=[comp['y'] - 0.35],
        mode='text',
        text=comp['perf'],
        textfont=dict(size=8, color='#13343B'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add layer labels on the left
layer_labels = [
    {'y': 6, 'text': 'Input Layer'},
    {'y': 4.5, 'text': 'Process Layer'},
    {'y': 3, 'text': 'Control Layer'},
    {'y': 1.5, 'text': 'Output Layer'},
    {'y': 0, 'text': 'Deploy Layer'}
]

for label in layer_labels:
    fig.add_trace(go.Scatter(
        x=[-0.2],
        y=[label['y']],
        mode='text',
        text=label['text'],
        textfont=dict(size=10, color='#13343B'),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add arrows using annotations
arrow_configs = [
    # Camera to MediaPipe
    {'x': 1.5, 'y': 5.25, 'ax': 2, 'ay': 6},
    # Camera to Gesture
    {'x': 2.5, 'y': 5.25, 'ax': 2, 'ay': 6},
    # MediaPipe to PyAutoGUI
    {'x': 1.5, 'y': 3.75, 'ax': 1, 'ay': 4.5},
    # Gesture to PyAutoGUI
    {'x': 2.5, 'y': 3.75, 'ax': 3, 'ay': 4.5},
    # PyAutoGUI to Desktop
    {'x': 2, 'y': 2.25, 'ax': 2, 'ay': 3},
    # Desktop to Python
    {'x': 1.5, 'y': 0.75, 'ax': 2, 'ay': 1.5},
    # Desktop to Electron
    {'x': 2.5, 'y': 0.75, 'ax': 2, 'ay': 1.5}
]

for arrow in arrow_configs:
    fig.add_annotation(
        x=arrow['x'], y=arrow['y'],
        ax=arrow['ax'], ay=arrow['ay'],
        xref='x', yref='y',
        axref='x', ayref='y',
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor='#13343B',
        showarrow=True
    )

# Update layout
fig.update_layout(
    title="CamMouse System Architecture",
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-1, 4]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        range=[-0.7, 6.7]
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12)
)

# Save the chart
fig.write_image("cammouse_architecture.png")
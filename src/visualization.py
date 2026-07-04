import plotly.graph_objects as go
import numpy as np

def plot_trajectory_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray, v: np.ndarray, t: dict, idx_max_v: int = 0) -> go.Figure:
    """
    Plots the 3D trajectory of the ball and draws a simplified volleyball court.
    """
    fig = go.Figure()
    
    # Plot trajectory
    fig.add_trace(go.Scatter3d(
        x=x, y=z, z=y, 
        mode='lines+markers',
        marker=dict(size=2, color='#000000'),
        line=dict(color='#E3000F', width=8),
        name=t["plot_traj"],
        customdata=v,
        hovertemplate="X: %{x:.2f} m<br>Z: %{y:.2f} m<br>Y: %{z:.2f} m<br>V: %{customdata:.2f} " + t["unit_v"] + "<extra></extra>"
    ))
    
    # Highlight max speed point
    fig.add_trace(go.Scatter3d(
        x=[x[idx_max_v]], y=[z[idx_max_v]], z=[y[idx_max_v]], 
        mode='markers',
        marker=dict(size=8, color='#000000', symbol='diamond', line=dict(color='#E3000F', width=2)),
        name='MAX SPEED',
        customdata=[v[idx_max_v]],
        hovertemplate="X: %{x:.2f} m<br>Z: %{y:.2f} m<br>Y: %{z:.2f} m<br>V_max: %{customdata:.2f} " + t["unit_v"] + "<extra></extra>"
    ))
    
    # Court dimensions (m)
    court_length = 18.0
    court_width = 9.0
    net_height = 2.43
    
    # Draw court (edges and surface)
    fig.add_trace(go.Mesh3d(
        x=[0, court_length, court_length, 0],
        y=[-court_width/2, -court_width/2, court_width/2, court_width/2],
        z=[0, 0, 0, 0],
        color='#999999',
        opacity=0.3,
        name=t["plot_court"]
    ))
    
    # Draw net (at x=9)
    fig.add_trace(go.Surface(
        x=[[court_length/2, court_length/2], [court_length/2, court_length/2]],
        y=[[-court_width/2, court_width/2], [-court_width/2, court_width/2]],
        z=[[0, 0], [net_height, net_height]],
        colorscale=[[0, '#555555'], [1, '#555555']],
        showscale=False,
        opacity=0.8,
        name=t["plot_net"]
    ))
    
    # Set layout
    fig.update_layout(
        title=dict(text=t["plot_title"], font=dict(family="Oswald, sans-serif", size=24)),
        scene=dict(
            xaxis_title=t["axis_x"],
            yaxis_title=t["axis_y"],
            zaxis_title=t["axis_z"],
            aspectmode='data',
            xaxis=dict(range=[-2, 20]),
            yaxis=dict(range=[-6, 6]),
            zaxis=dict(range=[0, 6])
        ),
        margin=dict(l=0, r=0, b=0, t=60)
    )
    
    return fig

def plot_speed_2d(time_arr: np.ndarray, v: np.ndarray, t: dict) -> go.Figure:
    """
    Plots a 2D line graph of Speed vs Time.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_arr, y=v,
        mode='lines',
        line=dict(color='#E3000F', width=4),
        name=t["axis_speed"],
        hovertemplate="T: %{x:.2f} s<br>V: %{y:.2f} " + t["unit_v"] + "<extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text=t["plot_speed_title"], font=dict(family="Oswald, sans-serif", size=20)),
        xaxis_title=t["axis_time"],
        yaxis_title=t["axis_speed"],
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig

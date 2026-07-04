import plotly.graph_objects as go
import numpy as np

def plot_trajectory_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray, v: np.ndarray, t: dict, idx_max_v: int = 0) -> go.Figure:
    """
    Plots an ANIMATED 3D trajectory of the ball with Plotly animation frames.
    The ball flies along the court with a growing trail and ground shadow.
    """
    court_length = 18.0
    court_width = 9.0
    net_height = 2.43

    # Subsample for performance (max ~60 frames)
    total_pts = len(x)
    step = max(1, total_pts // 60)
    indices = list(range(0, total_pts, step))
    if indices[-1] != total_pts - 1:
        indices.append(total_pts - 1)

    # ---------- base traces (index 0-4 will be updated in frames) ----------
    # 0: ball marker
    ball_trace = go.Scatter3d(
        x=[x[0]], y=[z[0]], z=[y[0]],
        mode='markers',
        marker=dict(size=10, color='#FFDD00', line=dict(color='#E3000F', width=3)),
        name='Мяч',
        showlegend=True
    )
    # 1: trail (growing line)
    trail_trace = go.Scatter3d(
        x=[x[0]], y=[z[0]], z=[y[0]],
        mode='lines',
        line=dict(color='#E3000F', width=6),
        name=t["plot_traj"],
        showlegend=True
    )
    # 2: shadow on floor (x-z projection at y=0)
    shadow_trace = go.Scatter3d(
        x=[x[0]], y=[z[0]], z=[0.0],
        mode='lines',
        line=dict(color='rgba(0,0,0,0.25)', width=3, dash='dot'),
        name='Тень',
        showlegend=False
    )
    # 3: max speed diamond
    max_speed_trace = go.Scatter3d(
        x=[x[idx_max_v]], y=[z[idx_max_v]], z=[y[idx_max_v]],
        mode='markers',
        marker=dict(size=7, color='#000000', symbol='diamond', line=dict(color='#E3000F', width=2)),
        name='MAX SPEED',
        customdata=[v[idx_max_v]],
        hovertemplate="V_max: %{customdata:.1f} " + t["unit_v"] + "<extra></extra>"
    )
    # 4: court surface
    court_trace = go.Mesh3d(
        x=[0, court_length, court_length, 0],
        y=[-court_width/2, -court_width/2, court_width/2, court_width/2],
        z=[0, 0, 0, 0],
        color='#999999', opacity=0.3,
        name=t["plot_court"]
    )
    # 5: net
    net_trace = go.Surface(
        x=[[court_length/2, court_length/2], [court_length/2, court_length/2]],
        y=[[-court_width/2, court_width/2], [-court_width/2, court_width/2]],
        z=[[0, 0], [net_height, net_height]],
        colorscale=[[0, '#555555'], [1, '#555555']],
        showscale=False, opacity=0.8,
        name=t["plot_net"]
    )

    fig = go.Figure(data=[ball_trace, trail_trace, shadow_trace, max_speed_trace, court_trace, net_trace])

    # ---------- animation frames ----------
    frames = []
    for k in indices:
        ball_frame = go.Scatter3d(x=[x[k]], y=[z[k]], z=[y[k]])
        trail_frame = go.Scatter3d(x=x[:k+1], y=z[:k+1], z=y[:k+1])
        shadow_frame = go.Scatter3d(x=x[:k+1], y=z[:k+1], z=np.zeros(k+1))
        frames.append(go.Frame(
            data=[ball_frame, trail_frame, shadow_frame],
            traces=[0, 1, 2],  # update only ball, trail, shadow
            name=str(k)
        ))

    fig.frames = frames

    # ---------- layout ----------
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
        margin=dict(l=0, r=0, b=0, t=60),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            x=0.05, y=0.05,
            xanchor="left", yanchor="bottom",
            buttons=[
                dict(label="▶ Play",
                     method="animate",
                     args=[None, dict(
                         frame=dict(duration=40, redraw=True),
                         fromcurrent=True,
                         transition=dict(duration=0)
                     )]),
                dict(label="⏸ Pause",
                     method="animate",
                     args=[[None], dict(
                         frame=dict(duration=0, redraw=False),
                         mode="immediate",
                         transition=dict(duration=0)
                     )])
            ]
        )],
        sliders=[dict(
            active=0,
            steps=[dict(args=[[str(k)], dict(
                frame=dict(duration=40, redraw=True),
                mode="immediate",
                transition=dict(duration=0)
            )], label="", method="animate") for k in indices],
            x=0.1, len=0.8,
            xanchor="left",
            y=0, yanchor="top",
            currentvalue=dict(visible=False),
            transition=dict(duration=0)
        )]
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

def plot_monte_carlo(points: list) -> go.Figure:
    """
    Plots the landing points of the Monte Carlo simulation on a 2D court representation.
    """
    fig = go.Figure()
    
    # Extract successes and failures
    x_succ, z_succ = [], []
    x_fail, z_fail = [], []
    
    for px, pz, is_succ in points:
        if is_succ:
            x_succ.append(px)
            z_succ.append(pz)
        else:
            x_fail.append(px)
            z_fail.append(pz)
            
    # Court background (opponent side: x from 9 to 18, z from -4.5 to 4.5)
    fig.add_shape(type="rect",
        x0=9, y0=-4.5, x1=18, y1=4.5,
        line=dict(color="black", width=2),
        fillcolor="rgba(150, 150, 150, 0.3)"
    )
    
    # Net line
    fig.add_shape(type="line",
        x0=9, y0=-4.5, x1=9, y1=4.5,
        line=dict(color="red", width=4)
    )
    
    # Scatter points
    if x_succ:
        fig.add_trace(go.Scatter(x=x_succ, y=z_succ, mode='markers', marker=dict(color='green', size=8), name="Успех"))
    if x_fail:
        fig.add_trace(go.Scatter(x=x_fail, y=z_fail, mode='markers', marker=dict(color='red', size=8, symbol='x'), name="Аут/Сетка"))
        
    fig.update_layout(
        title="Монте-Карло: Точки падения (Разброс)",
        xaxis_title="Длина корта (X, м)",
        yaxis_title="Ширина корта (Z, м)",
        xaxis=dict(range=[8, 20]),
        yaxis=dict(range=[-6, 6]),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    return fig

import math

from src.input_handler import SimulationParams, ServeType
from src.physics import solve_trajectory_3d
from src.config import G

def test_no_drag_parabola():
    """
    Test that without drag and without spin, the trajectory is a perfect parabola.
    """
    params = SimulationParams(
        v0=10.0,
        alpha_deg=45.0,
        y0=0.0,
        serve_type=ServeType.TOPSPIN,
        spin_rpm=0.0,
        cd=0.0 # No drag
    )
    
    t, x, y, z, vx, vy, vz = solve_trajectory_3d(params)
    
    # Distance should be v0^2 * sin(2*alpha) / g
    v0_x = 10.0 * math.cos(math.radians(45))
    v0_y = 10.0 * math.sin(math.radians(45))
    expected_distance = (v0_x * v0_y * 2) / G
    
    assert math.isclose(x[-1], expected_distance, rel_tol=1e-2)
    assert all(z == 0.0) # No lateral force
    
def test_topspin_shorter_than_float():
    """
    Topspin should fall shorter than a float serve with the same initial conditions
    due to downward Magnus force.
    """
    params_float = SimulationParams(
        v0=20.0,
        alpha_deg=15.0,
        y0=2.5,
        serve_type=ServeType.FLOAT,
        spin_rpm=0.0
    )
    t_f, x_f, y_f, z_f, vx_f, vy_f, vz_f = solve_trajectory_3d(params_float)
    
    params_topspin = SimulationParams(
        v0=20.0,
        alpha_deg=15.0,
        y0=2.5,
        serve_type=ServeType.TOPSPIN,
        spin_rpm=600.0
    )
    t_t, x_t, y_t, z_t, vx_t, vy_t, vz_t = solve_trajectory_3d(params_topspin)
    
    assert x_t[-1] < x_f[-1]

def test_hit_ground_event():
    params = SimulationParams(y0=2.0)
    t, x, y, z, vx, vy, vz = solve_trajectory_3d(params)
    
    # Final y should be approximately 0
    assert abs(y[-1]) < 0.1
    assert y[-1] >= -0.1 # Should not fall through the floor

"""
Physical constants and default configurations for Math_Model_3D.
"""
import math

# Environmental constants
G = 9.81  # Acceleration due to gravity (m/s^2)
RHO = 1.225  # Air density at sea level and 15°C (kg/m^3)

# Ball constants (Standard volleyball)
M_BALL = 0.27  # Mass of the ball (kg)
D_BALL = 0.21  # Diameter of the ball (m)
R_BALL = D_BALL / 2  # Radius of the ball (m)
A_BALL = math.pi * (R_BALL ** 2)  # Cross-sectional area (m^2)

# Aerodynamic constants
# Drag coefficient for a volleyball
# C_d is approx 0.4 in subcritical regime.
CD_DEFAULT = 0.4 

# Lift coefficient base for Magnus effect
CL_DEFAULT = 0.3 # Varies with spin parameter S = R*omega / v

# Strouhal number for Karman vortex street (Float serve)
STROUHAL_NUMBER = 0.2

import math
import random
from typing import Dict, List

def calculate_initial_velocity(S: float, t_flight: float) -> float:
    if t_flight <= 0: raise ValueError("Время полета должно быть больше нуля.")
    return S / t_flight

def calculate_impact_force(m: float, V0: float, dt_contact: float) -> float:
    if dt_contact <= 0: raise ValueError("Время контакта должно быть больше нуля.")
    return (m * V0) / dt_contact

def solve_trajectory_3d(V0: float, alpha_deg: float, m: float, y0: float, serve_type: str, spin_rpm: float) -> Dict[str, List[float]]:
    dt = 0.01
    g = 9.81
    rho = 1.225
    R = 0.105
    A = math.pi * R**2
    Cd = 0.4 # Коэффициент лобового сопротивления
    
    alpha_rad = math.radians(alpha_deg)
    u = V0 * math.cos(alpha_rad)
    v = V0 * math.sin(alpha_rad)
    w = 0.0 # Начальная боковая скорость
    x, y, z = 0.0, y0, 0.0
    
    t = 0.0
    x_vals, y_vals, z_vals, t_vals = [x], [y], [z], [t]
    
    # Вращение
    omega = spin_rpm * (2 * math.pi / 60.0)
    omega_vec = [0.0, 0.0, -omega] # Топспин вращается вокруг -Z
    
    # Параметры вихревой дорожки Кармана (для планера)
    D = 2 * R
    St = 0.2 # Число Струхаля
    phi_z = random.uniform(0, 2 * math.pi)
    phi_y = random.uniform(0, 2 * math.pi)
    
    while y >= 0 and x <= 25: 
        V_mag = math.sqrt(u**2 + v**2 + w**2)
        if V_mag == 0: break
        
        # 1. Лобовое сопротивление (Drag force)
        Fd_mag = 0.5 * rho * A * Cd * V_mag**2
        Fd_x = -Fd_mag * (u / V_mag)
        Fd_y = -Fd_mag * (v / V_mag)
        Fd_z = -Fd_mag * (w / V_mag)
        
        # 2. Эффект Магнуса (Для Topspin)
        Fm_x, Fm_y, Fm_z = 0.0, 0.0, 0.0
        if serve_type == 'topspin' and omega > 0:
            # Векторное произведение w x V
            cross_x = omega_vec[1]*w - omega_vec[2]*v
            cross_y = omega_vec[2]*u - omega_vec[0]*w
            cross_z = omega_vec[0]*v - omega_vec[1]*u
            
            cross_mag = math.sqrt(cross_x**2 + cross_y**2 + cross_z**2)
            if cross_mag > 0:
                Cm = 0.25 # Эмпирический коэффициент подъемной силы
                Fm_mag = 0.5 * rho * A * Cm * V_mag**2
                Fm_x = Fm_mag * (cross_x / cross_mag)
                Fm_y = Fm_mag * (cross_y / cross_mag)
                Fm_z = Fm_mag * (cross_z / cross_mag)
                
        # 3. Вихревая дорожка Кармана (Для Float)
        Fk_x, Fk_y, Fk_z = 0.0, 0.0, 0.0
        if serve_type == 'float':
            f_shedding = St * V_mag / D
            # Колеблющаяся подъемная и боковая сила
            Cl_z = 0.15 * math.sin(2 * math.pi * f_shedding * t + phi_z)
            Cl_y = 0.08 * math.sin(2 * math.pi * f_shedding * t + phi_y)
            
            Fk_z = 0.5 * rho * A * Cl_z * V_mag**2
            Fk_y = 0.5 * rho * A * Cl_y * V_mag**2

        # Сумма сил
        Fx = Fd_x + Fm_x + Fk_x
        Fy = -m * g + Fd_y + Fm_y + Fk_y
        Fz = Fd_z + Fm_z + Fk_z
        
        # Интегрирование Эйлера
        u += (Fx / m) * dt
        v += (Fy / m) * dt
        w += (Fz / m) * dt
        
        x += u * dt
        y += v * dt
        z += w * dt
        t += dt
        
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)
        t_vals.append(t)
        
    return {'t': t_vals, 'x': x_vals, 'y': y_vals, 'z': z_vals}

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List

def print_results(V0: float, F: float, serve_type: str) -> None:
    print("\n--- Результаты расчетов (V3 3D) ---")
    print(f"Тип подачи: {serve_type.upper()}")
    print(f"Начальная скорость V0: {V0:.2f} м/с ({(V0*3.6):.2f} км/ч)")
    print(f"Реальная сила удара F: {F:.2f} Ньютонов")

def plot_and_save_3d(trajectory: Dict[str, List[float]], serve_type: str, graphics_dir: Path) -> None:
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Траектория
    color = 'r' if serve_type == 'topspin' else 'b'
    ax.plot(trajectory['x'], trajectory['z'], trajectory['y'], label='Траектория', color=color, linewidth=2.5)
    
    # Отрисовка площадки (18x9 м)
    # Половина площадки (наша сторона) от 0 до 9, чужая от 9 до 18. Ширина от -4.5 до 4.5
    xx, zz = np.meshgrid([0, 18], [-4.5, 4.5])
    yy = np.zeros_like(xx)
    ax.plot_surface(xx, zz, yy, color='orange', alpha=0.3)
    
    # Отрисовка сетки (x=9, z от -4.5 до 4.5, y от 0 до 2.43)
    xx_net, yy_net = np.meshgrid([9, 9], [0, 2.43])
    zz_net = np.array([[-4.5, 4.5], [-4.5, 4.5]])
    ax.plot_surface(xx_net, zz_net, yy_net, color='gray', alpha=0.5, edgecolor='black')
    
    # Лицевая линия противника (x=18)
    ax.plot([18, 18], [-4.5, 4.5], [0, 0], color='white', linewidth=3)
    
    ax.set_xlabel('Длина площадки X (м)')
    ax.set_ylabel('Ширина Z (м)')
    ax.set_zlabel('Высота Y (м)')
    ax.set_title(f'3D Аэродинамика: Подача {serve_type.upper()}')
    
    ax.set_xlim(0, 20)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 5)
    ax.legend()
    
    graphics_dir.mkdir(parents=True, exist_ok=True)
    filename = graphics_dir / f"trajectory_3d_{serve_type}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n3D График сохранён как {filename}")

import argparse
from pathlib import Path

from src.input_handler import load_data_from_json, input_data_interactive
from src.physics import calculate_initial_velocity, calculate_impact_force, solve_trajectory_3d
from src.visualization import print_results, plot_and_save_3d

def main() -> None:
    print("=== Математическое моделирование подачи ===\n")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='Путь к JSON-файлу с параметрами')
    args = parser.parse_args()

    try:
        if args.config:
            config_path = Path(args.config)
            data = load_data_from_json(config_path)
            print(f"Данные загружены из {config_path}")
        else:
            data = input_data_interactive()

        V0 = calculate_initial_velocity(data['S'], data['t_flight'])
        F = calculate_impact_force(data['m'], V0, data['dt_contact'])
        
        print_results(V0, F, data['serve_type'])
        
        print("\nМоделируем 3D траекторию с учетом эффектов Магнуса и Кармана...")
        trajectory = solve_trajectory_3d(
            V0=V0, alpha_deg=data['alpha_deg'], m=data['m'], 
            y0=data['y0'], serve_type=data['serve_type'], spin_rpm=data['spin_rpm']
        )
        
        graphics_dir = Path(__file__).parent / 'graphics'
        plot_and_save_3d(trajectory, data['serve_type'], graphics_dir)

    except Exception as e:
        print(f"\nКритическая ошибка: {e}")

if __name__ == '__main__':
    main()

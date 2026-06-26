import json
from pathlib import Path
from typing import Dict, Any

def get_positive_float(prompt: str, default: float = None) -> float:
    while True:
        default_str = f" [{default}]" if default is not None else ""
        user_input = input(f"{prompt}{default_str}: ").strip()
        if not user_input and default is not None:
            return default
        try:
            val = float(user_input)
            if val >= 0:
                return val
            print("Значение не может быть отрицательным.")
        except ValueError:
            print("Некорректный ввод.")

def get_string(prompt: str, valid_options: list, default: str) -> str:
    while True:
        user_input = input(f"{prompt} ({'/'.join(valid_options)}) [{default}]: ").strip().lower()
        if not user_input:
            return default
        if user_input in valid_options:
            return user_input
        print("Выберите из предложенных вариантов.")

def input_data_interactive() -> Dict[str, Any]:
    print("\nИнтерактивный ввод параметров (3D Аэродинамика):")
    data = {}
    data['serve_type'] = get_string("Тип подачи", ['topspin', 'float'], 'topspin')
    data['spin_rpm'] = get_positive_float("Скорость вращения (об/мин)", default=(600 if data['serve_type']=='topspin' else 0))
    data['S'] = get_positive_float("Дистанция полета S (метры)")
    data['t_flight'] = get_positive_float("Время полета t (секунды)")
    data['m'] = get_positive_float("Масса мяча m (кг)", default=0.27)
    data['dt_contact'] = get_positive_float("Время контакта dt (секунды)", default=0.015)
    data['alpha_deg'] = get_positive_float("Угол вылета alpha (градусы)", default=12.0)
    data['y0'] = get_positive_float("Начальная высота вылета y0 (метры)", default=2.8)
    return data

def load_data_from_json(filepath: Path) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    required_keys = ['serve_type', 'spin_rpm', 'S', 't_flight', 'm', 'dt_contact', 'alpha_deg', 'y0']
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Отсутствует ключ: {key}")
    return data

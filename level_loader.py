import json
import os
from obstacles import Spike, Block

class LevelLoader:
    """Класс для загрузки структуры уровня из JSON-файла."""
    @staticmethod
    def load_level(filename, floor_y):
        if not os.path.exists(filename):
            print(f"Ошибка: Файл уровня {filename} не найден!")
            return "Unknown Level", 300, [], 8

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        level_name = data.get("level_name", "Без названия")
        speed = data.get("speed", 350)
        duration_seconds = data.get("duration_seconds", 2400 / speed)
        raw_objects = data.get("objects", [])

        obstacles_list = []

        for obj in raw_objects:
            obj_type = obj.get("type")
            x = obj.get("x")
            y = obj.get("y")

            if obj_type == "spike":
                spike = Spike(x, floor_y if y is None else y)
                obstacles_list.append(spike)
            elif obj_type == "block":
                # Создаем твердый блок
                block = Block(x, y)
                obstacles_list.append(block)

        return level_name, speed, obstacles_list, duration_seconds

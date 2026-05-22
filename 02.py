from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    printer_constraints = PrinterConstraints(**constraints)

    if printer_constraints.max_volume <= 0 or printer_constraints.max_items <= 0:
        raise ValueError("Обмеження принтера мають бути додатними.")

    for job in jobs:
        if job.volume <= 0 or job.print_time <= 0:
            raise ValueError("Об'єм моделі та час друку мають бути додатними.")
        if job.priority not in (1, 2, 3):
            raise ValueError("Пріоритет завдання повинен бути 1, 2 або 3.")
        if job.volume > printer_constraints.max_volume:
            raise ValueError(
                f"Модель {job.id} перевищує максимальний об'єм принтера."
            )

    # Вищий пріоритет друкується раніше, а для однакових пріоритетів
    # зберігаємо початковий порядок надходження.
    sorted_jobs = sorted(enumerate(jobs), key=lambda item: (item[1].priority, item[0]))

    print_order: List[str] = []
    total_time = 0
    current_batch: List[PrintJob] = []
    current_volume = 0.0

    def finalize_batch(batch: List[PrintJob]) -> int:
        if not batch:
            return 0
        return max(job.print_time for job in batch)

    for _, job in sorted_jobs:
        can_add_by_items = len(current_batch) < printer_constraints.max_items
        can_add_by_volume = current_volume + job.volume <= printer_constraints.max_volume

        if can_add_by_items and can_add_by_volume:
            current_batch.append(job)
            current_volume += job.volume
            continue

        total_time += finalize_batch(current_batch)
        print_order.extend(batch_job.id for batch_job in current_batch)

        current_batch = [job]
        current_volume = job.volume

    total_time += finalize_batch(current_batch)
    print_order.extend(batch_job.id for batch_job in current_batch)

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()

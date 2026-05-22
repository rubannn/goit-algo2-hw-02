import random
from typing import List, Tuple


def find_min_max(nums: List[int]) -> Tuple[int, int]:
    """Знаходить мінімальний і максимальний елементи методом розділяй і володарюй."""
    if not nums:
        raise ValueError("Масив не може бути порожнім.")

    def finder(left: int, right: int) -> Tuple[int, int]:
        if left == right:
            return nums[left], nums[left]

        if right - left == 1:
            if nums[left] < nums[right]:
                return nums[left], nums[right]
            return nums[right], nums[left]

        mid = (left + right) // 2
        left_min, left_max = finder(left, mid)
        right_min, right_max = finder(mid + 1, right)

        return min(left_min, right_min), max(left_max, right_max)

    return finder(0, len(nums) - 1)


def generate_random_array() -> List[int]:
    length = random.randint(10, 20)
    return [random.randint(-50, 50) for _ in range(length)]


if __name__ == "__main__":
    arr = generate_random_array()
    mn, mx = find_min_max(arr)

    print(f"Випадковий масив: {arr}")
    print(f"Мінімальний елемент: {mn}")
    print(f"Максимальний елемент: {mx}")

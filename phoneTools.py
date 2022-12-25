import time
import os

click_cords = []

active_color = 0  # 0 - white | 1 - black


# Активные координаты нажатия
def get_cords() -> list:
    return click_cords


# Активный цвет
def get_active_color() -> int:
    return active_color


# Смена цвета
def change_color(color: str) -> None:
    global active_color
    active_color = 1 if color == "black" else 0


def make_move(step: str):
    """Определение координат, куда нужно нажать по ходу"""
    cell = 135

    # Рокировки
    if step == "0-0":
        click(5 * cell - 45, (10 - 2) * cell - 45 + 711)  # при белых
        click(7 * cell - 45, (10 - 2) * cell - 45 + 711)  # при белых

        click(4 * cell - 45, (-1 + 8) * cell - 45 + 711)  # при черных
        click(2 * cell - 45, (-1 + 8) * cell - 45 + 711)  # при черных
        return
    if step == "0-0-0":
        click(5 * cell - 45, (10 - 2) * cell - 45 + 711)  # при белых
        click(3 * cell - 45, (10 - 2) * cell - 45 + 711)  # при белых

        click(4 * cell - 45, (-1 + 1) * cell - 45 + 711)  # при черных
        click(6 * cell - 45, (-1 + 1) * cell - 45 + 711)  # при черных
        return

    amogus = list("abcdefgh" if active_color == 0 else "hgfedcba")

    x1 = amogus.index(step[0]) + 1
    y1 = int(step[1]) + 1

    x2 = amogus.index(step[2]) + 1
    y2 = int(step[3]) + 1

    # клик на телефоне
    if active_color == 0:
        click(x1 * cell - 45, (10 - y1) * cell - 45 + 711)  # при белых
        click(x2 * cell - 45, (10 - y2) * cell - 45 + 711)  # при белых
    else:
        click(x1 * cell - 45, (-1 + y1) * cell - 45 + 711)  # при черных 
        click(x2 * cell - 45, (-1 + y2) * cell - 45 + 711)  # при черных


def click(x: int, y: int, delay=0.5) -> None:
    """Клик на телефоне + сохранение актуальных координат клика"""
    if len(click_cords) == 4:
        click_cords.clear()

    click_cords.append(x)
    click_cords.append(y)

    time.sleep(delay)
    os.system(f"adb\\adb shell input tap {x} {y}")

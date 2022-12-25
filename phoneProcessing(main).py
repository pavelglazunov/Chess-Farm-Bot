import sys
import time
import random
import cv2
import os
from datetime import datetime

from imageProcessing import get_board_matrix, are_we_white, crop_image
from chessProcessing import get_step, next_step, set_first_step_black, first_move, get_depth, get_board, get_evaluation, \
    get_move
from phoneTools import make_move, change_color, get_active_color, get_cords

from settings import *

move_count = 0  # счетчик ходов
time_coefficient = START_TIME_COEFFICIENT  # коэффициент для случайной задержки по времени

now_play = "p"  # p or b - активный игрок (p - реальный игрок, b - бот)


def beautiful_log(mc, ls, ns) -> None:
    """
    Логирование
    :param mc: move_count - номер хода
    :param ls: last_step - последний ход
    :param ns: new_step - найденный ход
    :return: print()
    """
    depth = get_depth()
    x1, y1, x2, y2 = get_cords()
    board = get_board()
    evl = get_evaluation()
    move = get_move()

    print(f"""
+- STEP № {mc} {'-' * (3 - len(str(mc)))}--------------------------+
| actual time wait: |{time_coefficient}     \t\t|
| actual depth:     |{depth}    \t\t|
+---------------------------------------+
| opponent step:    | {ls}      \t|
| best found step:  | {ns}      \t|
+---------------------------------------+
| moved from:       | x: {x1} | y: {y1} \t|
| moved to:         | x: {x2} | y: {y2} \t|
+---------------------------------------+
| POSITION | {'+' if evl['type'] == 'cp' else '-'} {evl['value']}
+----------+
{board}

    """)

    log = f"time: {datetime.now()}; move number: {mc}; depth: {depth}; wait time: {time_coefficient}; " \
          f"opponent step: {ls}; bot step: {ns}; click1: [x={x1}, y={y1}]; click2: [x={x2}, y={y2}]; moves: {move}\n"
    # file.write(log)


def start() -> None:
    # скриншот экрана телефона
    os.system("adb\\adb exec-out screencap -p > screenshot.png")
    img = cv2.imread("screenshot.png")

    playing_as_white = are_we_white(img)  # проверка на игру за белых\черных

    if not playing_as_white:
        set_first_step_black()  # подготовка доски к игре за черных
        change_color("black")  # установка игры за черных в phoneTools.py
    else:
        later = random.choice('abcdefgh')
        step_num = random.randint(1, 2)
        change_color("white")  # установка игры за белых в phoneTools.py
        first_move(f"{later}2{later}{2 + step_num}")  # первый ход за белых
        make_move(f"{later}2{later}{2 + step_num}")  # первый ход (вывод на доску)

    print(f"active color: {'white' if get_active_color() == 0 else 'black'}")


def main():
    global move_count, time_coefficient

    while True:
        if now_play == "p":
            # Если игра против игрока случайная задержка каждый ход + изменение задержки в зависимости от номера хода
            time.sleep(random.randint(1, time_coefficient))
            if move_count == 20:
                time_coefficient = 15
            if move_count == 30:
                time_coefficient = 30

            if time_coefficient == 50:
                time_coefficient = 6
        else:
            time.sleep(4)
            # pass
        # скриншот экрана телефона
        os.system("adb\\adb exec-out screencap -p > screenshot.png")
        img = cv2.imread("screenshot.png")

        # Обрезание скриншота в зависимости от оппонента
        if now_play == "p":
            img = crop_image(img, BOARD_RIGHT["p"], BOARD_TOP["p"], BOARD_SIZE, BOARD_SIZE)
        else:
            img = crop_image(img, BOARD_RIGHT["b"], BOARD_TOP["b"], BOARD_SIZE, BOARD_SIZE)

        active_board = get_board_matrix(img)  # получение матрицы игрового поля из скриншота

        last_step = get_step(active_board)  # определение хода, который сделал соперник

        # Если соперник не ходил пропуск цикла
        if not last_step:
            time.sleep(5)
            continue

        new_step = next_step(last_step)  # запись хода соперника в движок, получение лучшего хода

        if new_step == "mate":
            return

        make_move(new_step)  # вывод хода на телефон

        if SAVE_LOG:
            beautiful_log(mc=move_count, ls=last_step, ns=new_step)  # логирование последних событий

        move_count += 1


try:
    if __name__ == '__main__':
        if SAVE_LOG:
            file = open(f"logs/logs.txt", mode="a+")
            file.write("========== " + str(datetime.now()) + " ==========" + "\n")

        start()
        main()

    # file.close()
except Exception as e:
    print(f"Finish with error: {e}")
    if SAVE_LOG:
        file.write(f"ERROR: {e}")
        file.close()

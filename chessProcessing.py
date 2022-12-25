from stockfish import Stockfish
from phoneTools import get_active_color

depth = 18  # глубина анализа движка

# подключение движка
stockfish = Stockfish('stockfish')
stockfish.set_depth(depth)


# Актуальная глубина
def get_depth() -> int:
    return depth


# Актуальная доска
def get_board():
    return stockfish.get_board_visual()


# Актуальная оценка хода
def get_evaluation() -> dict:
    return stockfish.get_evaluation()


# Актуальный список ходов
def get_move() -> list:
    return moves


old_matrix = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
              ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
              ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
              ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

get_square = [
    ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
    ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
    ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
    ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
    ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
    ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
    ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
    ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']]

moves = []


def set_first_step_black() -> None:
    """Подготовка движка к игре за черных"""
    global old_matrix, get_square

    old_matrix = [['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
                  ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                  ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                  ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r']]

    for i in range(8):
        get_square[i] = list(reversed(get_square[i]))

    for i in range(4):
        for j in range(8):
            get_square[i][j], get_square[7 - i][j] = get_square[7 - i][j], get_square[i][j]

    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")


def get_step(new_matrix) -> str:
    """Получение последнего хода соперника путем сравнивания новой и старой матрицы поля"""
    global old_matrix

    # print(old_matrix)
    # print()
    # print(new_matrix)
    # TODO переделать обнаружение фигур

    steps = []
    for y in range(8):
        for x in range(8):
            if old_matrix[y][x] != new_matrix[y][x]:
                if new_matrix[y][x] == " ":
                    start_pos = get_square[y][x]
                else:
                    end_pos = get_square[y][x]
                steps.append(get_square[y][x])

    if len(steps) == 1:
        return ""
        # print(old_matrix)
        # print(steps, "?")
        # print(new_matrix)
        # raise ValueError("НАЙДЕН ТОЛЬКО ОДИН ХОД, СУУКА")

    if len(steps) == 2:
        old_matrix = new_matrix
        return f"{start_pos}{end_pos}"

    if len(steps) == 3:
        print(old_matrix)
        print(steps)
        print(new_matrix)
        return ""

    # Обработка рокировок
    print(steps)
    if get_active_color() == 0:
        if steps == ['a8', 'c8', 'd8', 'e8']:
            old_matrix = new_matrix
            return "e1c1"
        if steps == ['e8', 'f8', 'g8', 'h8']:
            old_matrix = new_matrix
            return "e8g8"

    else:
        if steps == ['h1', 'g1', 'f1', 'e1']:
            old_matrix = new_matrix
            return "e1g1"
        if steps == ['e1', 'f1', 'g1', 'h1']:
            old_matrix = new_matrix
            return "e1c1"
    # for step in steps:
    #     # if get_active_color() == 1:
    #         # if step[1] == "1":
    #
    #     if step[0] == "g":
    #         old_matrix = new_matrix
    #         if get_active_color() == 0 and step[1] == "1":
    #             return "e1g1"
    #         if get_active_color() == 0 and step[1] == "8":
    #             return "e8g8"
    #         if get_active_color() == 1 and step[1] == "1":
    #             return "e1g1"
    #         if get_active_color() == 1 and step[1] == "8":
    #             return "e8c8"
    #
    #     if step[0] == "c":
    #         old_matrix = new_matrix
    #         if get_active_color() == 0 and step[1] == "1":  #
    #             return "e1c1"
    #         if get_active_color() == 0 and step[1] == "8":
    #             return "e8c8"
    #         if get_active_color() == 1 and step[1] == "1":
    #             return "e1g1"
    #         if get_active_color() == 1 and step[1] == "8":
    #             return "e8g8"

    return ""


def first_move(step: str) -> None:
    """Первый ход за белых"""
    global moves
    moves.append(step)

    stockfish.set_position(moves)
    change_old_matrix(step)


def next_step(step: str) -> str:
    """Добавление хода соперника в движок + получение лучшего хода"""
    global moves
    moves.append(step)
    stockfish.set_position(moves)

    best_step = stockfish.get_best_move()
    moves.append(best_step)
    stockfish.set_position(moves)

    change_old_matrix(best_step)

    return best_step


def change_old_matrix(step: str) -> None:
    """Изменение значений старой матрицы по ходу"""

    # Рокировки
    if get_active_color() == 0:
        if step == "e1g1":
            old_matrix[7][4], old_matrix[7][7] = " ", " "
            old_matrix[7][6], old_matrix[7][5] = "K", "R"

        if step == "e1c1":
            old_matrix[7][0], old_matrix[7][4] = " ", " "
            old_matrix[7][2], old_matrix[7][3] = "K", "R"
    else:
        if step == "e8g8":
            old_matrix[7][0], old_matrix[7][3] = " ", " "
            old_matrix[7][1], old_matrix[7][2] = "k", "r"
        if step == "e8c8":
            old_matrix[7][3], old_matrix[7][7] = " ", " "
            old_matrix[7][4], old_matrix[7][5] = "r", "k"
    # if step == "e1g1":
    #     old_matrix[7][4], old_matrix[7][7] = " ", " "
    #     old_matrix[7][5], old_matrix[7][6] = "R", "K"
    #     return
    # if step == "e1c1":
    #     old_matrix[7][4], old_matrix[7][0] = " ", " "
    #     old_matrix[7][2], old_matrix[7][3] = "k", "r"
    #     return
    # if step == "e8g8":
    #     old_matrix[0][4], old_matrix[0][7] = " ", " "
    #     old_matrix[0][5], old_matrix[0][6] = "r", "k"
    #     return
    # if step == "e8c8":
    #     old_matrix[0][4], old_matrix[0][0] = " ", " "
    #     old_matrix[0][2], old_matrix[0][3] = "k", "r"
    #     return
    start_step, end_step = step[:2], step[2:]

    # Замена значений
    for i in get_square:
        for j in i:
            if start_step in j:
                y1, x1 = get_square.index(i), i.index(start_step)
            if end_step in j:
                y2, x2 = get_square.index(i), i.index(end_step)

    old_matrix[y2][x2] = old_matrix[y1][x1]
    old_matrix[y1][x1] = " "



"""
[['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'], 
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
['r', ' ', ' ', 'k', 'q', 'b', 'n', 'r']]

[['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'], 
['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], 
[' ', 'k', 'r', ' ', 'q', 'b', 'n', 'r']]



[[' ', 'K', 'R', ' ', 'Q', 'B', 'N', 'R'], 
['P', 'P', 'P', ' ', ' ', ' ', 'P', 'P'], 
[' ', ' ', ' ', 'P', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', 'P', 'B', ' ', ' '], 
[' ', ' ', ' ', 'N', ' ', 'p', ' ', ' '], 
[' ', ' ', 'n', 'p', ' ', ' ', ' ', 'p'], 
['p', 'p', 'p', ' ', ' ', 'q', 'p', ' '], 
['r', ' ', 'b', 'k', ' ', 'b', 'n', 'r']]
['c4'] ?
[[' ', 'K', 'R', ' ', 'Q', 'B', 'N', 'R'], 
['P', 'P', 'P', ' ', ' ', ' ', 'P', 'P'], 
[' ', ' ', ' ', 'P', ' ', ' ', ' ', ' '], 
[' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '], 
[' ', ' ', ' ', 'N', ' ', 'p', ' ', ' '], 
[' ', ' ', 'n', 'p', ' ', ' ', ' ', 'p'], 
['p', 'p', 'p', ' ', ' ', 'q', 'p', ' '], 
['r', ' ', 'b', 'k', ' ', 'b', 'n', 'r']]






[['r', ' ', ' ', 'q', 'r', ' ', 'k', ' '], 
['p', 'p', 'p', 'b', ' ', 'p', 'b', 'p'], 
[' ', ' ', ' ', 'p', ' ', 'n', 'p', ' '], 
[' ', ' ', ' ', ' ', 'n', ' ', ' ', ' '], 
[' ', ' ', 'P', 'N', 'P', ' ', ' ', ' '], 
[' ', ' ', 'N', ' ', 'B', 'P', ' ', ' '], 
['P', 'P', ' ', 'Q', 'B', ' ', 'P', 'P'], 
['R', ' ', ' ', ' ', ' ', 'R', ' ', ' ']]

[['r', ' ', ' ', 'q', 'r', ' ', 'k', ' '], 
['p', 'p', 'p', 'b', ' ', 'p', 'b', 'p'], 
[' ', ' ', ' ', 'p', ' ', ' ', 'p', ' '], 
[' ', ' ', ' ', ' ', 'n', ' ', ' ', 'n'], 
[' ', ' ', 'P', 'N', 'P', ' ', ' ', ' '], 
[' ', ' ', 'N', ' ', 'B', 'P', ' ', ' '], 
['P', 'P', ' ', 'Q', 'B', ' ', 'P', 'P'], 
['R', ' ', ' ', ' ', ' ', 'R', 'K', ' ']]


"""
import cv2
import numpy

pixels = {
    (22, 61): [
        [91, 91, 91, "K"],
        [49, 49, 50, "k"]
    ],
    (25, 45): [
        [247, 247, 247, "Q"],
        [110, 110, 113, "q"]
    ],
    (43, 36): [
        [74, 81, 77, "R"],
        [88, 91, 91, "R"],
        [60, 63, 63, "r"],
        [44, 52, 48, "r"]
    ],
    (96, 91): [
        [155, 155, 155, "N"],
        [55, 55, 56, "n"]
    ],
    (45, 82): [
        [248, 248, 248, "B"],
        [82, 83, 86, "b"]
    ],
    (66, 77): [
        [229, 229, 229, "P"],
        [74, 75, 78, "p"]
    ],
}


def check(img) -> str:
    """Определение фигуры на изображении (передается изображение только одной клетки)
    Определяет при помощи заранее выбранного пикселя (координаты и цвет)"""
    for i in pixels.keys():
        pixel = img[i[0], i[1]]

        for j in pixels[i]:
            b, g, r, n = j
            if (pixel[0] == b) and (pixel[1] == g) and (pixel[2] == r):
                return n

    return " "


def crop_image(image, x, y, width, height):
    """Разрезка изображения"""
    return image[y:y + height, x:x + width]


def get_board_matrix(img):
    """Составление матрицы поля путем разрезания на клетки и определения фигур на каждой из них"""
    width, height = img.shape[1], img.shape[0]
    cell = int(width / 8)

    board = [[" " for i in range(8)] for j in range(8)]
    for y in range(8):
        for x in range(8):
            cell_img = img[y * cell:y * cell + cell, x * cell:x * cell + cell]
            board[y][x] = check(cell_img)
    return board


def are_we_white(image) -> bool:
    """Проверка на игру за белых, если белые - True, иначе - False"""
    pixel = image[1730, 60]
    return pixel[0] == 248 and pixel[1] == 248 and pixel[2] == 248


def compare_images(image1, image2):
    """Сравнение двух изображений"""
    return image1.shape == image2.shape and not (numpy.bitwise_xor(image1, image2).any())

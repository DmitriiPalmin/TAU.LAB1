import numpy as num
import matplotlib.pyplot as pyplot
import sympy as simp
import control.matlab as matlab
import math as m
import colorama as color

# выбор звена
container_name = dict()
container_name = {1: "Безынерционное звено", 2: "Апериодическое звено",
                  3: "Интегрирующее звено", 4: "Дифференциальное звено", 5: "Реальное дифференциальное звено"}


def choice():

    need_new_choice = True

    while need_new_choice:

        print(color.Style.RESET_ALL)

        user_input = input('Введите номер команды: \n'
                        '1 - ' + container_name[1] + ';\n'
                        '2 - ' + container_name[2] + ';\n'
                        '3 - ' + container_name[3] + ';\n'
                        '4 - ' + container_name[4] + ';\n'
                        '5 - ' + container_name[5] + ';\n')
        # Проверяем, число ли было введено

        if not user_input.isdigit() or int(user_input)>5 or int(user_input) == 0:
            print(color.Fore.RED + '\nНедопустимое значение')
        else:
            user_input = int(user_input)
            need_new_choice = False

    return container_name[user_input]

def getUnit(name):
    k = input("Введите коэффициент k: ")
    t = input("Введите коэффициент t: ")

    need_new_choice = True

    while need_new_choice:

        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            need_new_choice = False
            if name == container_name[1]:
                unit = matlab.tf([k], [1])
            elif name == container_name[2]:
                unit = matlab.tf([k], [t, 1])
            elif name == container_name[3]:
                unit = matlab.tf([1], [t, 0])
            elif name == container_name[4]:
                unit = matlab.tf([k, 0], [0.00000000001, 1])
            elif name == container_name[5]:
                unit = matlab.tf([k, 0], [t, 1])

        else:
            print(color.Fore.RED + 'Пожалуйста, введите числовое значение')
            need_new_choice = True

        print(unit)
    return unit

unit_name = choice()
unit = getUnit(unit_name)

def graph(num, title, y, x):
    pyplot.subplot(2,1, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'purple')
    elif title == 'Импульсная характеристика':
        pyplot.plot(x, y, 'green')
    pyplot.title(title)
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время (с)')
#
#
#
#
timeLine = []
for i in range(0, 10000):
    timeLine.append(i/1000)

[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная характеристика', y, x )
[y, x] = matlab.impulse(unit, timeLine)

graph(2, 'Импульсная характеристика', y, x )

pyplot.show()
import numpy as num
import matplotlib.pyplot as pyplot
import sympy as simp
import control.matlab as matlab
import math as m
import colorama as color

# выбор звена
def choice():
    inertialess_Unit_name = 'Безынерционное звено'
    aperiodic_Unit_name = 'Апериодическое звено'

    need_new_choice = True

    while need_new_choice:

        print(color.Style.RESET_ALL)

        user_input = input('Введите номер команды: \n'
                       '1 - ' + inertialess_Unit_name + ';\n'
                       '2 - ' + aperiodic_Unit_name + ';\n')
        # Проверяем, число ли было введено
        if user_input.isdigit():
            need_new_choice = False
            user_input = int(user_input)
            if user_input == 1:
                name = 'Безынерционное звено'
            elif user_input == 2:
                name = 'Апериодическое звено'
            else:
                print(color.Fore.RED + '\nНедопустимое значение')
                need_new_choice = True
        else:
            print (color.Fore.RED + 'Пожалуйста, введите числовое значение')
            need_new_choice = True
    return name

def getUnit(name):
    k = input("Введите коэффициент k: ")
    t = input("Введите коэффициент t: ")

    need_new_choice = True

    while need_new_choice:

        if k.isdigit() and t.isdigit():
            k = int(k)
            t = int(t)
            need_new_choice = False
            if name == 'Безынерционное звено':
                unit = matlab.tf([k], [1])
            elif name == 'Апериодическое звено':
                unit = matlab.tf([k], [t, 1])
        else:
            print(color.Fore.RED + 'Пожалуйста, введите числовое значение')
            need_new_choice = True
    return unit
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


unit_name = choice()
unit = getUnit(unit_name)

timeLine = []
for i in range(0, 10000):
    timeLine.append(i/1000)

[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная характеристика', y, x )
[y, x] = matlab.impulse(unit, timeLine)

graph(2, 'Импульсная характеристика', y, x )

pyplot.show()
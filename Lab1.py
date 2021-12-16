import control.matlab as c
import matplotlib.pyplot as plt
import sys
import numpy as np
from sympy import *
import math
import colorama as color

def choice():

    need_new_choice = True

    while need_new_choice:

        print(color.Style.RESET_ALL)

        user_input = input('Введите номер команды: \n'
                        '1 - Переходная характеристика;\n' 
                        '2 - Остальное;\n' )
        # Проверяем, число ли было введено

        if not user_input.isdigit() or int(user_input)>2 or int(user_input) == 0:
            print(color.Fore.RED + '\nНедопустимое значение')
        else:
            user_input = int(user_input)
            need_new_choice = False

    return user_input

# Пропорциональный регулятор
def PReg(Kp):
    wP = c.tf([Kp], [1])
    return wP


# Интегральный (интегрирующий) регулятор (интегратор)
def IReg(Ki):
    wI = c.tf([Ki], [1, 0])
    return wI


# Дифференциальный регулятор (дифференциатор)
def DReg(Kd):
    wD = c.tf([Kd, 0], [1])
    return wD


# Пропорционально-интегральный регулятор
def PIReg(Kp, Ki):
    wP = PReg(Kp)
    wI = IReg(Ki)
    wPI = c.parallel(wP + wI)
    return wPI


# Пропорционально-дифференциальный регулятор
def PDReg(Kp, Kd):
    wP = PReg(Kp)
    wD = DReg(Kd)
    wPD = c.parallel(wP + wD)
    return wPD


# Пропорционально-интегрально-дифференциальный регулятор
def PIDReg(Kp, Ki, Kd):
    wP = PReg(Kp)
    wI = IReg(Ki)
    wD = DReg(Kd)
    wPID = c.parallel(wP + wI + wD)
    return wPID


def CAY(wFunctionList, wReg):
    w5 = c.tf([1], [1])
    for i in wFunctionList:
        w5 = c.series(w5, i)
    w5 = c.series(w5, wReg)
    w = c.feedback(w5, 1, -1)
    return w


def step(wFunctionList, wNameList):
    f = True
    yPerehHar = []
    xPerehHar = []
    TimeLine = []
    for i in range(0, 600, 1):
        TimeLine.append(i / 10)
    plt.figure(figsize=(6, 6))
    for i in wFunctionList:
        y, x = c.step(i, TimeLine)
        plt.plot(x, y)
        yPerehHar.append(y)
        xPerehHar.append(x)
    plt.hlines(y[590], 0, 60, color='r', linewidth=0.5, linestyle='-')
    plt.vlines(26, 0, y[590]+0.05, color='b', linewidth=0.75, linestyle='-')
    plt.hlines(y[590]+0.05, 0, 60, color='g', linewidth=0.5, linestyle='--')
    plt.hlines(y[590]-0.05, 0, 60, color='g', linewidth=0.5, linestyle='--')
    # plt.hlines(1, 0, 60, color='r', linewidth=0.5, linestyle='-')
    # plt.vlines(26, 0, 1.05, color='b', linewidth=0.75, linestyle='-')
    # plt.hlines(1.05, 0, 60, color='g', linewidth=0.5, linestyle='--')
    # plt.hlines(0.95, 0, 60, color='g', linewidth=0.5, linestyle='--')
    plt.legend(wNameList, fontsize=10)
    plt.title('Переходная характеристика ')
    plt.ylabel('Амплитуда', fontsize=10, color='black')
    plt.xlabel('Время(сек)', fontsize=8, color='black')
    plt.grid()
    # plt.show()
    return yPerehHar, xPerehHar

# АЧХ
def ACH(wFunctionList, wNameList):
    omeg = []
    magList = []
    for i in range(1, 1000, 1):
        omeg.append(i / 10)
    for i in wFunctionList:
        mag, phase, omega = c.bode(i, omeg, dB=False)
        magList.append(mag)
        plt.legend(wNameList, fontsize=10, shadow=True)
        plt.plot()
        plt.show()
    return magList

def tregACH(magList):
    treg = 2*((2*3.14)/(magList[0]))
    return treg


def kolebACH(magList):
    # i = 1
    maxMag = magList[0]
    for i in range(len(magList)):
        if magList[i] >= magList[i-1]:
            maxMag = magList[i]
    M = maxMag/magList[0]
    return M

# ЛАЧХ и ЛФЧХ
def LACH(w, wNameList):
    magList = []
    omegaList = []
    phaseList = []
    magListF = []
    omegaListF = []
    phaseListF = []
    # for i in wFunctionList:
    mag, phase, omega = c.bode(w, dB=True)
    for j in range(len(mag)):
        magList.append(20*(math.log10(mag[j])))
        omegaList.append(omega[j]/(2*math.pi))
        phaseList.append(math.degrees(phase[j]))
    plt.legend(wNameList, fontsize=10)
    plt.plot()
    plt.show()
    omegaListF.append(omegaList)
    magListF.append(magList)
    phaseListF.append(phaseList)

    return omegaListF, magListF, phaseListF


def zapasL(omegaList, magList, phaseList):
    maxMag = magList[0]
    for j in range(len(magList)):
        if (magList[j] <= 0) and (magList[j-1] >= 0):
            y2 = phaseList[j]
            break
    phase = 180 - abs(y2)
    print("Запас устойчивости по фазе через ЛАЧХ и ЛФЧХ = ",phase)
    k = 0
    for i in range(len(phaseList)):
        if phaseList[i] == 180:
            k = 1
            indexMaxPhase = i
            break
    if k == 1:
        ampl = abs(0 - magList[indexMaxPhase])
    else:
        ampl = abs(0 - magList[-1])
    print("Запас устойчивости по амплитуде через ЛАЧХ и ЛФЧХ = ", ampl)


# проверка по корням и расположение корней на комплексной плоскости
def root_f(w, map=False) -> object:
    korni = []
    f = 0
    s = c.pole(w)
    for i in s:
        if (i.real > 0):
            f = 1
            break
        elif (i.real == 0):
            f = 2
    if (f == 1):
        print("Система неустойчива по корням")
    elif (f == 2):
        print("Система на границе устойчивости по корням")
    else:
        print("Система устойчива по корням")
    for i in s:
        korni.append(i)
        print(i, ' ')
    if map:
        c.pzmap(w)
        plt.axis([-5, 0.5, -2, 2])
        plt.show()
    return korni

def int_err(y, ust, dt):
    I1_List = []
    I2_List = []
    I1 = 0
    I2 = 0
    for i in y:
        for j in i:
            # интегральная ошибка
            I1 = sqrt((ust-j)*(ust-j))*dt + I1
            # квадратичная интегральная ошибка
            I2 = (ust - j) * (ust - j) * dt + I2
        I1_List.append(I1)
        I2_List.append(I2)
    return I1_List, I2_List


def treg_h(y, x, ust, dot):
    gr1 = ust + (ust * dot)
    gr2 = ust - (ust * dot)
    lastY = 0.0
    lastX = 0.0
    lastYList = []
    lastXList = []
    for i in range(len(x)):
        for j in range(len(y[i])):
            if ((y[i][j-1] >= gr1) and (y[i][j] <= gr1)) \
                    or ((y[i][j-1] <= gr2) and (y[i][j] >= gr2)):
                lastY = y[i][j]
                lastX = x[i][j]
        lastYList.append(lastY)
        lastXList.append(lastX)
    return lastYList, lastXList

def perereg_h(y, ust):
    maxY = 0.0
    perereg_List = []
    for i in y:
        for j in i:
            if (j >= maxY):
                maxY = j
        perereg = (maxY - ust)/(ust)
        perereg = perereg*100
        perereg_List.append(perereg)
    return perereg_List

def koleb_h(yPerehHar, xPerehHar, treg):
    kMax = 0
    kMaxList = []

    for i in range(len(yPerehHar)):
        for j in range(len(yPerehHar[i])):
            if (xPerehHar[i][j] == treg):
                break
            if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
                kMax+=1
        kMaxList.append(kMax)
        if len(kMaxList) > 1:
            g = kMaxList[0]/kMaxList[1]
            print (g)
    return kMaxList

def zatuh_f(y, x, treg):
    yMaxList = []
    zatuhList = []

    for i in range(len(y)):
        for j in range(len(y[i])):
            if (x[i][j] == treg):
                break
            if (y[i][j] > y[i][j - 1]) and (y[i][j] > y[i][j + 1]):
                yMax = y[i][j]
                yMaxList.append(yMax)
        yMaxList.append(0)
        if yMaxList[1] != 0:
            zatuh = (yMaxList[1]-yMaxList[0])/(yMaxList[1])
            zatuhList.append(abs(zatuh))
        else:
            zatuh = 1
            zatuhList.append(zatuh)
    return zatuhList


def max_f(yPerehHar, xPerehHar):
    tMaxList = []
    yMaxList = []
    yMax = 0.0

    for i in range(len(yPerehHar)):
        for j in range(len(yPerehHar[i])):
            if (yPerehHar[i][j] > yMax):
                yMax = yPerehHar[i][j]
                tMax = xPerehHar[i][j]
    tMaxList.append(tMax)
    yMaxList.append(yMax)
    return yMaxList, tMaxList

def tregroot(roots):
    reKorni = []
    for i in roots:
        reKorni.append(re(i))
    for j in range(len(reKorni)):
        if (abs(reKorni[j]) <= abs(reKorni[j-1])):
            reKorniMin = reKorni[j]
    treg = 3/(abs(reKorniMin))
    return treg

def kolebroot(korni):
    imk = []
    rek = []
    max = abs(im(korni[0]) / re(korni[0]))
    for i in range(len(korni)):
        imk.append(im(korni[i]))
        rek.append(re(korni[i]))
    max = abs(imk[0]/rek[0])
    for j in range(len(korni)):
        g = abs((imk[j]/rek[j]))
        print (g)
        if max < g:
            max = g

    return max

def pereregroot(sk):
    sigma = math.e**((math.pi)/sk)
    return sigma

def zatuhroot(sk):

    stepzatuh = 1 - math.e**((-2*(math.pi))/sk)
    return stepzatuh


ky = 20.0
Tg = 10.0
Ty = 5.0
Tgm = 2.0
w1 = c.tf([1],[Tg,1])
w2 = c.tf([Tgm*0.01,1],[Tg*0.05,1])
w3 = c.tf([ky],[Ty,1])
wraz = c.series(w1,w2,w3)

# task = choice()
task=2
wReg = PIDReg(0.9, 0.006, 0.90)
# wReg = PDReg(1, 1.3)

W = CAY([w1, w2, w3], wReg)
print("W(p) = ", W)
if task == 1:
    yh, xh = step([W], ["W(p)"])
    y = yh[0]
    I1, I2 = int_err(yh, y[599], 0.05)

    print("Интегральная ошибка I1= ", I1[0], "\n"
         "Квадратичная интегральная ошибка I2= ", I2[0])
    lastYW, lastXW = treg_h(yh, xh, y[599], 0.05)
    print("tрег= ", lastXW[0])
    perereg = perereg_h(yh, 1)
    print("Перерегулирование = ", perereg[0], "%")
    koleb = koleb_h (yh, xh, lastXW[0])
    print("Колебательность = ", koleb[0])
    zatuh = zatuh_f(yh, xh, lastXW[0])
    print("Степень затухания = ", zatuh[0])
    yMax, tMax = max_f(yh, xh)
    print("Величина достижения первого максимума = ", yMax[0])
    print("Время достижения первого максимума = ", tMax[0])
if task == 2:

    roots = root_f(W, map=true)

    omegaListF, magListF, phaseListF = LACH(W, ["W(p)"])
    zapasL(omegaListF[0], magListF[0], phaseListF[0])
    magListFACH = ACH([W], ["W(P)"])
    tregACH = tregACH(magListFACH[0])
    print("Время регулирования по АЧХ = ", tregACH)
    kolebM = kolebACH(magListFACH[0])
    print("Показатель колебательности М = ", kolebM)
    treg = tregroot(roots)
    print("Время регулирования по корням= ", treg)
    kolebr = kolebroot(roots)
    print("Степень колебательности по корням= ", kolebr)
    sigma = pereregroot(kolebr)
    print("Перерегулирование переходной характеристики по корням= ", sigma)
    zatuhr = zatuhroot(kolebr)
    print("Степень затухания по корням= ",zatuhr)






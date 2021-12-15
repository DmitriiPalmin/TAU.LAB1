import control.matlab as c
import matplotlib.pyplot as plt
import sys
import numpy as np
from sympy import *
import math


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


def perehodnay(wFunctionList, wNameList):
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
        # for i in range(len(yPerehHar)):
        #     for j in range(len(yPerehHar[i])):
        #         print(yPerehHar[i][j], "-", xPerehHar[i][j], "\n")
    plt.vlines(13, 0, 1.05, color='b', linewidth=0.75, linestyle='-')
    plt.hlines(1, 0, 60, color='r', linewidth=0.5, linestyle='-')
    plt.hlines(1.05, 0, 60, color='g', linewidth=0.5, linestyle='--')
    plt.hlines(0.95, 0, 60, color='g', linewidth=0.5, linestyle='--')
    plt.legend(wNameList, fontsize=10, shadow=True)
    plt.title('Переходная характеристика ')
    plt.ylabel('Амплитуда', fontsize=10, color='black')
    plt.xlabel('Время(сек)', fontsize=8, color='black')
    plt.grid()
    plt.show()
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


def pokazatelkolebACH(magList, ustavka):
    i = 1
    maxMag = magList[0]
    for i in range(len(magList)):
        if magList[i] >= magList[i-1]:
            maxMag = magList[i]
    M = maxMag/ustavka
    return M

# ЛАЧХ и ЛФЧХ
def LACH(wFunctionList, wNameList):
    magList = []
    omegaList = []
    phaseList = []
    magListF = []
    omegaListF = []
    phaseListF = []
    for i in wFunctionList:
        mag, phase, omega = c.bode(i, dB=True)
        k = 0
        j = 0
        for j in range(len(mag)):
            magList.append(20*(math.log10(mag[j])))
            omegaList.append(omega[j]/(2*math.pi))
            phaseList.append(math.degrees(phase[j]))
        plt.legend(wNameList, fontsize=10, shadow=True)
        plt.plot()
        plt.show()
    omegaListF.append(omegaList)
    magListF.append(magList)
    phaseListF.append(phaseList)
    return omegaListF, magListF, phaseListF


def zapasustoichivostiLachLfch(omegaList, magList, phaseList):
    maxMag = magList[0]
    for i in range(len(magList)):
        if magList[i]>=maxMag:
            maxMag = magList[i]
            indexMaxMag = i
    j = indexMaxMag
    for j in range(len(magList)):
        if (magList[j] <= 0) and (magList[j-1] >= 0):
            # x2 = omegaList[j]
            # x1 = omegaList[j-1]
            y2 = phaseList[j]
            # y1 = phaseList[j-1]
            # z2 = magList[j]
            # z1 = magList[j-1]
            break
    fase = 180 - abs(y2)
    print("Запас устойчивости по фазе через ЛАЧХ и ЛФЧХ = ",fase)
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
def pokorn(w, map=False):
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

def ikvosh(yPerehHar, ustavka, dt):
    I1List=[]
    I2List = []
    I1 = 0
    I2 = 0
    for i in yPerehHar:
        for j in i:
            I1 = sqrt((ustavka-j)*(ustavka-j))*dt + I1      #интегральная ошибка
            I2 = (ustavka - j) * (ustavka - j) * dt + I2    #квадратичная интегральная ошибка
        I1List.append(I1)
        I2List.append(I2)
    return I1List, I2List


def tregpereh(yPerehHar, xPerehHar, ustavka, toch):
    granica1 = ustavka + (ustavka * toch)
    granica2 = ustavka - (ustavka * toch)
    lastY = 0.0
    lastX = 0.0
    lastYList = []
    lastXList = []
    j=1
    for i in range(len(xPerehHar)):
        for j in range(len(xPerehHar[i])):
            if ((yPerehHar[i][j-1] >= granica1) and (yPerehHar[i][j] <= granica1)) \
                    or ((yPerehHar[i][j-1] <= granica2) and (yPerehHar[i][j] >= granica2)):
                lastY = yPerehHar[i][j]
                lastX = xPerehHar[i][j]
        lastYList.append(lastY)
        lastXList.append(lastX)
    return lastYList, lastXList

def pereregpereh(yPerehHar, ustavka):
    maxY = 0.0
    pereregulirovanieList = []
    for i in yPerehHar:
        for j in i:
            if (j >= maxY):
                maxY = j
        pereregulirovanie = (maxY - ustavka)/(ustavka)
        pereregulirovanie = pereregulirovanie*100
        pereregulirovanieList.append(pereregulirovanie)
    return pereregulirovanieList

def kolebatelnostpereh(yPerehHar, xPerehHar, treg):
    kMax = 0
    kMaxList = []
    j = 1
    for i in range(len(yPerehHar)):
        for j in range(len(yPerehHar[i])):
            if (xPerehHar[i][j] == treg):
                break
            if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
                kMax+=1
        kMaxList.append(kMax)
    return kMaxList

def stepenzatuhaniya(yPerehHar, xPerehHar, treg):
    yMaxList = []
    stepenzatuhaniyaList = []
    j = 1
    for i in range(len(yPerehHar)):
        for j in range(len(yPerehHar[i])):
            if (xPerehHar[i][j] == treg):
                break
            if (yPerehHar[i][j] > yPerehHar[i][j - 1]) and (yPerehHar[i][j] > yPerehHar[i][j + 1]):
                yMax = yPerehHar[i][j]
                yMaxList.append(yMax)
        yMaxList.append(0)
        if yMaxList[1] != 0:
            stepenzatuhaniya = (yMaxList[1]-yMaxList[0])/(yMaxList[1])
            stepenzatuhaniyaList.append(abs(stepenzatuhaniya))
        else:
            stepenzatuhaniya = 1
            stepenzatuhaniyaList.append(stepenzatuhaniya)
    return stepenzatuhaniyaList


def yMaxtMax(yPerehHar, xPerehHar):
    tMaxList = []
    yMaxList = []
    yMax = 0.0
    j = 1
    for i in range(len(yPerehHar)):
        for j in range(len(yPerehHar[i])):
            if (yPerehHar[i][j] > yMax):
                yMax = yPerehHar[i][j]
                tMax = xPerehHar[i][j]
    tMaxList.append(tMax)
    yMaxList.append(yMax)
    return yMaxList, tMaxList

def tregkorni(korni):
    reKorni = []
    j = 1
    for i in korni:
        reKorni.append(re(i))
    for j in range(len(reKorni)):
        if (abs(reKorni[j]) <= abs(reKorni[j-1])):
            reKorniMin = reKorni[j]
    treg = 3/(abs(reKorniMin))
    return treg

def stepenkolebkorni(korni):
    i = 1
    for i in range(len(korni)):
        if (abs(korni[i]) >= abs(korni[i-1])):
            maxkoren = korni[i]
    remaxkoren = re(maxkoren)
    immaxkoren = im(maxkoren)
    stepenkoleb = math.tan(math.radians(abs(immaxkoren)/abs(remaxkoren)))
    return stepenkoleb

def pereregkorni(korni):
    maxkoren = korni[0]
    i = 1
    for i in range(len(korni)):
        if (abs(korni[i]) >= abs(korni[i-1])):
            maxkoren = korni[i]
    remaxkoren = re(maxkoren)
    immaxkoren = im(maxkoren)
    stepenkoleb = abs(immaxkoren/remaxkoren)
    sigma = math.e**((math.pi)/stepenkoleb)
    return sigma

def stepzatuhkorni(korni):
    maxkoren = korni[0]
    i = 1
    for i in range(len(korni)):
        if (abs(korni[i]) >= abs(korni[i-1])):
            maxkoren = korni[i]
    remaxkoren = re(maxkoren)
    immaxkoren = im(maxkoren)
    stepenkoleb = math.tan(math.radians(abs(immaxkoren)/abs(remaxkoren)))
    stepzatuh = 1 - math.e**((-2*math.radians(math.pi))/stepenkoleb)
    return stepzatuh


ky = 22.0
Tg = 5.0
Ty = 4.0
Tgm = 1.0
w1 = c.tf([1],[Tg,1])
print("Wг = ", w1)
w2=c.tf([Tgm*0.01,1],[Tg*0.05,1])
print("Wпт = ", w2)
w3 = c.tf([ky],[Ty,1])
print("Wиу = ", w3)
w = c.series(w1,w2,w3)
# W = CAY([w1, w2, w3], wReg=PIDReg(1,0,0))
# print("W(p) = ", W)
# yPerehHarW, xPerehHarW = perehodnay([W], ["W(p)"])
# omegaListF, magListF, phaseListF = LACH([W], ["W(p)"])
# korniW = pokorn(W, map=true)
W = CAY([w1, w2, w3], wReg=PIDReg(0.2506, 0.03488, 0.3259))
print("W(p) = ", W)
yPerehHarW, xPerehHarW = perehodnay([W], ["W(p)"])
I1, I2 = ikvosh(yPerehHarW, 1, 0.05)
print("Интегральная ошибка I1= ", I1[0], "\nКвадратичная интегральная ошибка I2= ", I2[0])
lastYW, lastXW = tregpereh(yPerehHarW, xPerehHarW, 1, 0.05)
print("tрег= ", lastXW[0])
pereregulirovanie = pereregpereh(yPerehHarW, 1)
print("Перерегулирование= ", pereregulirovanie[0], "%")
kolebatelnostperehW = kolebatelnostpereh(yPerehHarW, xPerehHarW, lastXW[0])
print("Колебательность= ", kolebatelnostperehW[0])
stepenzatuhaniya = stepenzatuhaniya(yPerehHarW, xPerehHarW, lastXW[0])
print("Степень затухания= ", stepenzatuhaniya[0])
yMax, tMax = yMaxtMax(yPerehHarW, xPerehHarW)
print("Величина достижения первого максимума= ", yMax[0])
print("Время достижения первого максимума= ", tMax[0])

omegaListF, magListF, phaseListF = LACH([W], ["W(p)"])
zapasustoichivostiLachLfch(omegaListF[0], magListF[0], phaseListF[0])
magListFACH = ACH([W], ["W(P)"])
tregACH = tregACH(magListFACH[0])
print("treg по ACH = ", tregACH)
pokazatelkolebM = pokazatelkolebACH(magListFACH[0], 1)
print("Показатель колебательности М = ", pokazatelkolebM)
korniW = pokorn(W, map=true)
treg = tregkorni(korniW)
print("Время регулирования по корням= ", treg)
stepenkoleb = stepenkolebkorni(korniW)
print("Степень колебательности по корням= ", stepenkoleb)
sigma = pereregkorni(korniW)
print("Перерегулирование переходной характеристики по корням< ", sigma)
stepzatuhkorniW = stepzatuhkorni(korniW)
print("Степень затухания по корням= ",stepzatuhkorniW)


# W2 = CAY([w1, w2, w3], wReg=PReg(0.2725))
# W1 = CAY([w1, w2, w3], wReg=PReg(0.4525))
# yPerehHarW1W2W3 = perehodnay([W1, W2], ["W1(p)", "W2(p)"])



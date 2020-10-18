import random as rd
from random import randint
import math as mth
import numpy as np


# deklarasi chromose binary
def chromosome(chromosomeLength):
    return [randint(0, 1) for x in range(2 * chromosomeLength)]


# deklarasi populasi
def population(populationSize, chromosomeLength):
    return [chromosome(chromosomeLength) for x in range(populationSize)]


# decode populasi
def decode(listKromosom, xMax, xMin, chromosomeLength):
    maxSum = 0
    for i in range(0, chromosomeLength):
        maxSum += mth.pow(2, -(i + 1))
    sum = 0
    for k in range(0, chromosomeLength):
        sum += listKromosom[k] * mth.pow(2, -(k + 1))
    decimal = xMin + (xMax - xMin / maxSum) * sum
    return decimal


# fitness
def fitness(nilaiX1, nilaiX2, nilaiAcak):
    f = mth.cos(nilaiX1) * mth.sin(nilaiX2) - (nilaiX1 / (mth.pow(nilaiX2, 2) + 1))
    return 1 / (f + nilaiAcak)


# roulette wheel selection
def seleksiOrangTua(fitness):
    maxSum = 0
    for i in range(len(fitness)):
        maxSum += fitness[i]
    r = rd.random()
    indv = 0
    index = 0
    fitnessCek = 0
    while indv <= len(fitness):
        fitnessCek = fitnessCek + fitness[indv]
        if (fitnessCek / maxSum) > r:
            index = indv
            break
        indv += 1
    return index


# single point crossover
def rekombinasi(parent1, parent2, panjangKromosom):
    titikPotong = randint(1, ((2 * panjangKromosom) - 1))
    return parent1[0:titikPotong] + parent2[titikPotong : (2 * panjangKromosom)]


# mutasi genetik
def mutasi(kromosom, panjangKromosom, permutasi):
    mutasiKromosom = kromosom
    rand = rd.random()
    for i in range((2 * panjangKromosom)):
        if rand < permutasi:
            if kromosom[i] == 0:
                kromosom[i] = 1
            else:
                kromosom[i] = 0
        else:
            continue
    return mutasiKromosom


# GA Parameter
x1_max = 2
x1_min = -1
x2_max = 1
x2_min = -1
populasiAwal = []
x_generation = []
bestSoFar = 0
bestKromosom = []
bestVariable = []
fitnessList = []

# inisialisasi populasi
banyakPopulasi = 100
panjangKromosom = 3
isDone = True
populasiAwal = population(banyakPopulasi, panjangKromosom)
while isDone:
    for i in range(banyakPopulasi):
        nilaiKromosom = populasiAwal[i]
        nilaiX1 = decode(
            nilaiKromosom[:panjangKromosom], x1_max, x1_min, panjangKromosom
        )
        nilaiX2 = decode(
            nilaiKromosom[panjangKromosom:], x2_max, x2_min, panjangKromosom
        )
        if (nilaiX1 >= -1 and nilaiX1 <= 2) or (nilaiX2 >= -1 and nilaiX2 <= 1):
            fitnessValue = fitness(nilaiX1, nilaiX2, 0.05)
            x_generation.append(nilaiKromosom)
            fitnessList.append(fitnessValue)
            if fitnessValue > bestSoFar:
                bestSoFar = round(fitnessValue)
                bestVariable = [nilaiX1, nilaiX2]
                bestKromosom = [nilaiKromosom]
        else:
            continue
    if bestSoFar >= 20:
        print(bestVariable, bestSoFar)
        print("New Generation has Born")
        isDone = False
    else:
        populasiBaru = []
        for i in range(banyakPopulasi):
            seleksi1 = seleksiOrangTua(fitnessList)
            seleksi2 = seleksiOrangTua(fitnessList)
            parent1 = x_generation[seleksi1]
            parent2 = x_generation[seleksi2]
            anak = rekombinasi(parent1, parent2, panjangKromosom)
            mutasiGenetik = mutasi(anak, panjangKromosom, 0.05)
            populasiBaru.append(mutasiGenetik)
        print(bestVariable, bestSoFar)
        print("New Generation has Born")
        populasiAwal = populasiBaru


import math
import random
from random import randint


# inisialisasi chromosome integer
def chromosome(panjangKromosom):
    return [randint(0, 9) for x in range(panjangKromosom)]


# inisialisasi populasi
def population(panjangKromosom, banyakPopulasi):
    return [chromosome(panjangKromosom) for x in range(banyakPopulasi)]


# decode kromosom
def decode(xmax, xmin, kromosom):
    maxSum = 0
    for i in range(0, len(kromosom)):
        maxSum += 9 * (pow(10, -(i + 1)))
    kromosomValue = 0
    for j in range(0, len(kromosom)):
        kromosomValue += kromosom[j] * (pow(10, -(j + 1)))
    decimal = xmin + ((xmax - xmin) * kromosomValue / (maxSum))
    return round(decimal)


# fitness function
def fitness(nilaiX1, nilaiX2, nilaiAcak):
    f = (math.cos(nilaiX1) * math.sin(nilaiX2)) - (nilaiX1 / (math.pow(nilaiX2, 2) + 1))
    return math.pow(nilaiAcak, -f)


# seleksi orangtua dengan Roulette Wheel
def roulleteWheel(fitness):
    maxSum = 0
    for i in range(len(fitness)):
        maxSum += fitness[i][1]
    r = random.random()
    indv = 0
    index = 0
    fitnessCek = 0
    while indv <= len(fitness):
        fitnessCek = fitnessCek + fitness[indv][1]
        if (fitnessCek / maxSum) > r:
            index = indv
            break
        indv += 1
    return index


# rekombinasi anak
def rekombinasi(parent1, parent2, panjangKromosom):
    titikPotong = random.randint(1, panjangKromosom - 1)
    child1 = parent1[0:titikPotong] + parent2[titikPotong:panjangKromosom]
    child2 = parent2[0:titikPotong] + parent1[titikPotong:panjangKromosom]
    child = [child1, child2]
    return child


# mutasi anak
def mutasi(anak, probabilitasMutasi):
    for i in range(len(anak)):
        rd = random.random()
        if rd < probabilitasMutasi:
            anak[i] = randint(0, 9)
    return anak


# cari best fitness
def bestFitness(population):
    max = 0
    idx = -1
    for i in range(len(population)):
        cek = population[i][1]
        if cek > max:
            max = cek
            idx = i
    return max, population[idx][0]


# cari seleksi yang terbaik
def elitism(population):
    bestLokal = []
    bestLokal = bestFitness(population)
    return bestLokal


# GA Parameter
x1_max = 2
x1_min = -1
x2_max = 1
x2_min = -1
bestSoFar = 0
x_generation = []

# menampilkan nilai heuristik
def nilaiHeuristik(x1, x2):
    return (math.cos(x1) * math.sin(x2)) - (x1 / (math.pow(x2, 2) + 1))


# inisialisasi generasi awal
banyakPopulasi = 50
panjangKromosom = 10
panjangFenotipe = panjangKromosom // 2
isDone = True
iterasiPopulasi = 0
stagnantCek = [True, 0, 0]
genCounter = 1

listKromosom = population(panjangKromosom, banyakPopulasi)
while isDone and stagnantCek[0]:
    for i in range(len(listKromosom)):
        kromosomSaatini = listKromosom[i]
        x1 = decode(x1_max, x1_min, kromosomSaatini[0 : panjangFenotipe - 1])
        x2 = decode(x2_max, x2_min, kromosomSaatini[panjangFenotipe:panjangKromosom])
        fitnessValue = fitness(x1, x2, 10)
        x_generation.append([kromosomSaatini, fitnessValue])
    bestSoFar = elitism(x_generation)
    if genCounter >= 10000:
        isDone = False
    if stagnantCek[1] == bestSoFar[0]:
        stagnantCek[2] += 1
        if stagnantCek[2] >= 50:
            stagnantCek[0] = False
            isDone = False
    else:
        newPop = []
        stagnantCek[1] = bestSoFar[0]
        stagnantCek[2] = 0
        newPop.append(bestSoFar[1])
        for j in range(len(listKromosom)):
            seleksi1 = roulleteWheel(x_generation)
            seleksi2 = roulleteWheel(x_generation)
            parent1 = x_generation[seleksi1][0]
            parent2 = x_generation[seleksi2][0]
            anak = rekombinasi(parent1, parent2, panjangKromosom)
            for x in anak:
                newGen = mutasi(x, 0.9)
                newPop.append(newGen)
        listKromosom = newPop
    genCounter += 1

# output hasil terbaik
kromosomSaatini = bestSoFar[1]
x1 = decode(x1_max, x1_min, kromosomSaatini[0 : panjangFenotipe - 1])
x2 = decode(x2_max, x2_min, kromosomSaatini[panjangFenotipe:panjangKromosom])
print("Generasi Pertama Kali Ditemukan : ", genCounter - 50)
print("Generasi Saat Nilai Memenuhi Keadaan : ", genCounter)
print("Banyak Populasi : ", banyakPopulasi)
print("Panjang Kromosom : ", panjangKromosom)
print("Kromosom Terbaik ; ", kromosomSaatini)
print(
    "Fenotipe Terbaik : [ x1 = ",
    x1,
    ", x2 =",
    x2,
    "] ",
    " Nilai Fitness : ",
    bestSoFar[0],
)
print("Nilai Heuristik dari Fenotipe : ", nilaiHeuristik(x1, x2))
k = input("Press Enter To Close")


# NAMA : SYA RAIHAN HEGGI
# NIM : 1301184219
# KELAS : IF-42-03

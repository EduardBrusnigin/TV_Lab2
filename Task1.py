from random import random


print("""===========================================================================
ЗАДАНИЕ 1 (Вариант 21)

Вероятность изготовления годной детали из каждой отливки независимо от других равна p.
Случайная величина η — число использованных отливок для
изготовления годной детали.

P(η = k) = p*(1 - p)^(k-1), k = 1, 2, 3, 4, 5, ...
===========================================================================""")

p = 1.01

while (p < 0 or p > 1):
    p = float(input("Введите значение p: "))

    if p < 0:
        print("Вероятность не может быть меньше 0.")

    elif p > 1:
        print("Вероятность не может быть больше 1.")

print(f"\nЗаданное значение p: p = {p}\n")


n = -1

while (n <= 0):
    n = int(input("Введите значение n -- число экспериментов: "))

    if n <= 0:
        print("Число экспериментов должно быть больше 0.")

print(f"\nЗаданное значение n: n = {n}\n")



def interval(datchik):
    s = 0
    a = p
    j = 1

    while datchik >= s:
        s += a

        if datchik < s:
            return j

        a *= 1 - p
        j += 1



etha = {}

for i in range(n):
    datchik = random()

    j = interval(datchik)

    if not (j in etha):
        etha[j] = 1

    else:
        etha[j] += 1

etha = dict(sorted(etha.items()))


def print_dict_table(d):
    rows = [
        [str(k) for k in d],
        [str(v) for v in d.values()],
        [str(v / n) for v in d.values()],
    ]

    total = len(d)
    cols_per_row = 20
     
    for start in range(0, total, cols_per_row):
        end = start + cols_per_row
        chunk_rows = [row[start:end] for row in rows]
        widths = [max(len(str(cell)) for cell in col) for col in zip(*chunk_rows)]

        sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        print(sep)
        for row in chunk_rows:
            print("| " + " | ".join(f"{c:<{w}}" for c, w in zip(row, widths)) + " |")
            print(sep)
        


print_dict_table(etha)    

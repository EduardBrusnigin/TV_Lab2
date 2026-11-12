from random import random
import matplotlib.pyplot as plt


print("""===========================================================================
ЗАДАНИЕ 2 (Вариант 21)

Вероятность изготовления годной детали из каждой отливки независимо
от других равна p.
Случайная величина eta — число использованных отливок для
изготовления годной детали.
P(eta = k) = p * (1 - p)^(k-1),  k = 1, 2, 3, ...
===========================================================================""")


p = 1.01

while p <= 0 or p > 1:
    p = float(input("Введите значение p: "))
    if p <= 0:
        print("Вероятность должна быть больше 0.")
    elif p > 1:
        print("Вероятность не может быть больше 1.")

print(f"\nЗаданное значение p: p = {p}\n")


n = -1

while n <= 0:
    n = int(input("Введите число экспериментов n: "))
    if n <= 0:
        print("Число экспериментов должно быть больше 0.")

print(f"Заданное значение n: n = {n}\n")



def interval(u, p):
    s = 0.0
    a = p
    j = 1
    while u >= s:
        s += a
        if u < s:
            return j
        a *= (1 - p)
        j += 1


xs = [interval(random(), p) for _ in range(n)]
xs_sorted = sorted(xs)



x_bar = 0.0
for x in xs:
    x_bar += x
x_bar /= n

S2 = 0.0
for x in xs:
    S2 += (x - x_bar) ** 2
S2 /= n

x_min = xs_sorted[0]
x_max = xs_sorted[-1]
R = x_max - x_min

if n % 2 == 1:
    Me = xs_sorted[n // 2]
else:
    Me = (xs_sorted[n // 2 - 1] + xs_sorted[n // 2]) / 2.0



E_eta = 1.0 / p
D_eta = (1.0 - p) / (p * p)


print("=" * 64)
print("ТАБЛИЦА ЧИСЛОВЫХ ХАРАКТЕРИСТИК")
print("=" * 64)
print(f"{'Характеристика':<34} {'Значение':>15}")
print("-" * 64)
print(f"{'E(eta)':<34} {E_eta:>15.6f}")
print(f"{'x_bar':<34} {x_bar:>15.6f}")
print(f"{'|E(eta) - x_bar|':<34} {abs(E_eta - x_bar):>15.6f}")
print(f"{'D(eta)':<34} {D_eta:>15.6f}")
print(f"{'S^2':<34} {S2:>15.6f}")
print(f"{'|D(eta) - S^2|':<34} {abs(D_eta - S2):>15.6f}")
print(f"{'Me':<34} {Me:>15.6f}")
print(f"{'R':<34} {R:>15.6f}")
print("=" * 64)


freq = {}
for x in xs:
    freq[x] = freq.get(x, 0) + 1
ys = sorted(freq.keys())

print("\n" + "=" * 64)
print("ТАБЛИЦА: y_j, P(eta = y_j), n_j/n, отклонения")
print("=" * 64)
print(f"{'y_j':>6} {'P(eta=y_j)':>15} {'n_j/n':>15} {'|n_j/n-P|':>15}")
print("-" * 64)

max_dev = 0.0
for y in ys:
    Py = p * (1 - p) ** (y - 1)
    nj_n = freq[y] / n
    dev = abs(nj_n - Py)
    if dev > max_dev:
        max_dev = dev
    print(f"{y:>6} {Py:>15.6f} {nj_n:>15.6f} {dev:>15.6f}")
print("=" * 64)
print(f"max_j |n_j/n - P(eta=y_j)| = {max_dev:.6f}")


def F_theory(x, p):
    if x <= 1:
        return 0.0

    k = int(x)

    if k < x:
        k += 1

    return 1.0 - (1.0 - p) ** (k - 1)


def F_theory_right(x, p):
    if x < 1:
        return 0.0

    return 1.0 - (1.0 - p) ** int(x)


def F_empirical(x, xs_sorted, n):
    cnt = 0

    for v in xs_sorted:
        if v < x:
            cnt += 1
        else:
            break

    return cnt / n



x_plot = x_max + 2
while F_theory(x_plot + 1, p) < 0.99 and x_plot < 100000:
    x_plot += 1

x_grid = list(range(0, x_plot + 1))
y_theory = [F_theory(k, p) for k in x_grid]
y_emp = [F_empirical(k, xs_sorted, n) for k in x_grid]

plt.figure(figsize=(10, 6))
plt.step(x_grid, y_theory, where="pre", linewidth=2, color="blue",
         label="Теоретическая F(x)")
plt.step(x_grid, y_emp, where="pre", linestyle="--", color="orange",
         label="Выборочная F^(x)")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.title("Теоретическая и выборочная функции распределения")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



D = 0.0
for j in range(1, n + 1):
    xj = xs_sorted[j - 1]
    Fj_left = F_theory(xj, p)
    Fj_right = F_theory_right(xj, p) 
    d1 = j / n - Fj_right
    d2 = Fj_left - (j - 1) / n
    if d1 > D:
        D = d1
    if d2 > D:
        D = d2

print(f"\nМера расхождения D = sup |F^(x) - F(x)| = {D:.6f}")

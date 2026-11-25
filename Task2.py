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

p = -1.0
while p <= 0 or p > 1:
    p = float(input("Введите значение p (0 < p <= 1): "))
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

# --- Генерация выборки ---
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

# --- Расчет числовых характеристик (без библиотек) ---
x_bar = sum(xs) / n

S2 = sum((x - x_bar) ** 2 for x in xs) / n  # По методичке делитель n

x_min = xs_sorted[0]
x_max = xs_sorted[-1]
R = x_max - x_min

if n % 2 == 1:
    Me = float(xs_sorted[n // 2])
else:
    Me = (xs_sorted[n // 2 - 1] + xs_sorted[n // 2]) / 2.0

# Теоретические значения для геометрического распределения
E_eta = 1.0 / p
D_eta = (1.0 - p) / (p * p)

# --- Таблица 1: Числовые характеристики ---
print("=" * 85)
print("ТАБЛИЦА ЧИСЛОВЫХ ХАРАКТЕРИСТИК")
print("=" * 85)
# Вывод в одну строку, как в образце методички, или блоком для читаемости
print(f"{'E(eta)':<10} {'x_bar':<10} {'|E-x_bar|':<10} {'D(eta)':<10} {'S^2':<10} {'|D-S^2|':<10} {'Me':<10} {'R':<10}")
print("-" * 85)
print(f"{E_eta:<10.4f} {x_bar:<10.4f} {abs(E_eta - x_bar):<10.4f} {D_eta:<10.4f} {S2:<10.4f} {abs(D_eta - S2):<10.4f} {Me:<10.4f} {R:<10.4f}")
print("=" * 85)

# --- Таблица 2: Для дискретной с.в. (пункт А методички) ---
freq = {}
for x in xs:
    freq[x] = freq.get(x, 0) + 1
ys = sorted(freq.keys())

print("\n" + "=" * 70)
print("ТАБЛИЦА: y_j, P(eta = y_j), n_j/n, отклонения")
print("=" * 70)
print(f"{'y_j':>6} | {'P(eta=y_j)':>12} | {'n_j/n':>12} | {'|n_j/n - P|':>12}")
print("-" * 70)

max_dev = 0.0
for y in ys:
    Py = p * (1 - p) ** (y - 1)
    nj_n = freq[y] / n
    dev = abs(nj_n - Py)
    if dev > max_dev:
        max_dev = dev
    print(f"{y:>6} | {Py:>12.6f} | {nj_n:>12.6f} | {dev:>12.6f}")
print("-" * 70)
print(f"max_j |n_j/n - P(eta=y_j)| = {max_dev:.6f}")
print("=" * 70)

# --- Функции распределения ---
def F_theory(x, p):
    if x < 1:           # ИСПРАВЛЕНО: строгое неравенство
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

# --- Построение графика ---
x_plot = x_max + 2
while F_theory(x_plot + 1, p) < 0.99 and x_plot < 100000:
    x_plot += 1

x_grid = list(range(0, x_plot + 1))
y_theory = [F_theory(k, p) for k in x_grid]
y_emp = [F_empirical(k, xs_sorted, n) for k in x_grid]

plt.figure(figsize=(10, 6))
plt.step(x_grid, y_theory, where="post", linewidth=2, color="blue", label="Теоретическая F(x)")
plt.step(x_grid, y_emp, where="post", linestyle="--", color="orange", label="Выборочная F^(x)")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.title("Теоретическая и выборочная функции распределения (Вариант 21)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Расчет меры расхождения D (Колмогоров) ---
D = 0.0
for j in range(1, n + 1):
    xj = xs_sorted[j - 1]
    Fj_left = F_theory(xj, p)          # F(x_j)
    Fj_right = F_theory_right(xj, p)   # F(x_j + 0)
    
    d1 = j / n - Fj_right
    d2 = Fj_left - (j - 1) / n
    
    if d1 > D:
        D = d1
    if d2 > D:
        D = d2

print(f"\nМера расхождения D = sup |F^(x) - F(x)| = {D:.6f}")
print("===========================================================================")

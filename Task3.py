import math

print("""===========================================================================
ЗАДАНИЕ 3 - Проверка гипотезы о виде распределения (критерий Пирсона χ²)
С.в. η — число использованных отливок для изготовления годной детали.
Геометрическое распределение: P(eta = k) = p * (1 - p)^(k-1), k = 1, 2, 3, ...
===========================================================================""")



p = -1.0
while p <= 0 or p > 1:
    p = float(input("Введите значение вероятности p (0 < p <= 1): "))
    if p <= 0 or p > 1:
        print("Ошибка: вероятность должна быть в интервале (0, 1].")

n = -1
while n <= 0:
    n = int(input("Введите число экспериментов n: "))
    if n <= 0:
        print("Ошибка: число экспериментов должно быть больше 0.")



def generate_geometric(u, prob):
    s = 0.0
    a = prob
    j = 1
    while u >= s:
        s += a
        if u < s:
            return j
        a *= (1 - prob)
        j += 1


xs = [generate_geometric(random(), p) for random in (__import__('random').random for _ in range(n))]

print(f"\nВыборка сгенерирована: n = {n}, p = {p}")



k = -1
while k < 2:
    k = int(input("\nВведите число интервалов k (k >= 2): "))
    if k < 2:
        print("Ошибка: число интервалов должно быть не менее 2.")

print(f"Для разбиения на {k} интервалов введите {k-1} границу(z_1, z_2, ..., z_{k-1}).")
print("Рекомендация: для дискретной с.в. используйте границы вида 1.5, 2.5, 3.5 и т.д.")


z = [0.0] * (k + 1)
z[0] = -float('inf')
z[k] = float('inf')

for i in range(1, k):
    z[i] = float(input(f"Введите границу z_{i}: "))



def F_geom(x, prob):
    if x < 1:
        return 0.0
    return 1.0 - (1.0 - prob) ** int(x)


q = [] 
n_j = [] 
components = []

print("\n" + "=" * 90)
print("ТАБЛИЦА ИНТЕРВАЛОВ, ЧАСТОТ И ТЕОРЕТИЧЕСКИХ ВЕРОЯТНОСТЕЙ")
print("=" * 90)
print(f"{'Интервал j':<10} | {'Границы':<20} | {'n_j':<8} | {'q_j':<12} | {'n*q_j':<10} | {'Вклад в χ²':<12}")
print("-" * 90)

R0 = 0.0
eps = 1e-9

for j in range(k):

    prob_left = F_geom(z[j] - eps, p) if z[j] != -float('inf') else 0.0
    prob_right = F_geom(z[j+1] - eps, p) if z[j+1] != float('inf') else 1.0
    q_j = prob_right - prob_left
    q.append(q_j)
    

    count = 0
    for x_val in xs:
        if z[j] <= x_val < z[j+1]:
            count += 1
    n_j.append(count)
    

    nq = n * q_j
    if nq > 0:
        contrib = (count - nq) ** 2 / nq
        components.append(contrib)
        R0 += contrib
    else:
        components.append(0.0)
        

    left_str = "-∞" if z[j] == -float('inf') else f"{z[j]:.2f}"
    right_str = "∞" if z[j+1] == float('inf') else f"{z[j+1]:.2f}"
    
    print(f"Интервал {j+1:<5} | [{left_str:>6}, {right_str:<6}) | {count:<8} | {q_j:<12.6f} | {nq:<10.2f} | {components[j]:<12.6f}")

print("-" * 90)
print(f"Статистика Пирсона R0 = Σ (n_j - n*q_j)² / (n*q_j) = {R0:.6f}")
print("=" * 90)


small_nq = sum(1 for nq in [n * q_j for q_j in q] if nq < 5)
if small_nq > 0:
    print(f"\n⚠️ ВНИМАНИЕ: В {small_nq} интервал(ах) ожидаемая частота n*q_j < 5.")
    print("Это может снизить точность критерия χ². Рекомендуется объединить интервалы (уменьшить k).")



alpha = -1.0
while alpha <= 0 or alpha >= 1:
    alpha = float(input("\nВведите уровень значимости alpha (например, 0.05): "))
    if alpha <= 0 or alpha >= 1:
        print("Ошибка: alpha должно быть строго между 0 и 1.")


r = k - 1


def calculate_chi2_upper_tail(R0_val, r_val):
    p_param = r_val / 2.0
    x_param = R0_val / 2.0
    
    if x_param == 0:
        return 1.0 
        

    term = (math.exp(-x_param) * (x_param ** p_param)) / math.gamma(p_param + 1)
    sum_I = term
    
    m = 1

    while term > 1e-12 and m < 10000:
        term *= x_param / (p_param + m)
        sum_I += term
        m += 1
        

    return 1.0 - sum_I

F_R0 = calculate_chi2_upper_tail(R0, r)


print("\n" + "=" * 70)
print("РЕЗУЛЬТАТЫ ПРОВЕРКИ ГИПОТЕЗЫ")
print("=" * 70)
print(f"Число степеней свободы (r = k - 1): {r}")
print(f"Вычисленное значение статистики R0: {R0:.6f}")
print(f"Вычисленное значение F(R0) (p-value): {F_R0:.6f}")
print(f"Заданный уровень значимости alpha:   {alpha:.6f}")
print("-" * 70)


if F_R0 < alpha:
    print("ВЫВОД: F(R0) < alpha")
    print("РЕШЕНИЕ: ОТВЕРГНУТЬ нулевую гипотезу H0.")
    print("Данные статистически значимо расходятся с теоретическим распределением.")
else:
    print("ВЫВОД: F(R0) >= alpha")
    print("РЕШЕНИЕ: ПРИНЯТЬ нулевую гипотезу H0.")
    print("Расхождения между выборочными и теоретическими частотами незначимы.")
print("=" * 70)

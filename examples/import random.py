# Ввод массива с клавиатуры
n = int(input("Введите размер массива: "))
arr = []

print("Введите элементы массива:")
for i in range(n):
    arr.append(int(input(f"arr[{i}] = ")))

print("Ваш массив:")
print(arr)

# Поиск пар отрицательных элементов
first_pair_index = -1
last_pair_index = -1

for i in range(n - 1):
    if arr[i] < 0 and arr[i + 1] < 0:
        if first_pair_index == -1:
            first_pair_index = i
        last_pair_index = i

# Вывод результата
if first_pair_index != -1:
    print(f"Есть соединённые отрицательные элементы.")
    print(f"Первая пара: индексы {first_pair_index} и {first_pair_index + 1}")
    print(f"Последняя пара: индексы {last_pair_index} и {last_pair_index + 1}")
else:
    print("Соединённых отрицательных элементов нет.")
def levenshtein_distance(s, t):
  m = len(s)
  n = len(t)
  
  # Создаем матрицу размера (m+1)x(n+1) и заполняем ее нулями
  d = [[0 for _ in range(n+1)] for _ in range(m+1)]

  # Инициализируем первый столбец и первую строку матрицы
  for i in range(1, m+1):
    d[i][0] = i
  for j in range(1, n+1):
    d[0][j] = j

  # Заполняем матрицу согласно алгоритму Левенштейна
  for j in range(1, n+1):
    for i in range(1, m+1):
      if s[i-1] == t[j-1]:
        substitution_cost = 0
      else:
        substitution_cost = 1

      d[i][j] = min(d[i-1][j] + 1,                 # удаление
                    d[i][j-1] + 1,                 # вставка
                    d[i-1][j-1] + substitution_cost)  # замена

  return d

a = 'Кривцов'
b = 'Кризцов'

d = levenshtein_distance(a, b)
for row in d[1:]:
  for elem in row[1:]:
    print(elem, end=' ')
  print()
# print(levenshtein_distance(a, b))



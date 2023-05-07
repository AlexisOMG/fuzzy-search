def levenshtein_distance(s, t, k):
  # Check length difference
  if abs(len(s) - len(t)) > k:
    return float('inf')
  
  # Swap strings if necessary so that s is the shorter string
  if len(s) > len(t):
    s, t = t, s
  
  # Initialize distance array
  d = [0] * (len(s) + 1)
  
  # Calculate Levenshtein distance
  for j in range(1, len(t) + 1):
    prev = d[0]
    d[0] = j
    for i in range(1, len(s) + 1):
      old = d[i]
      cost = (s[i - 1] != t[j - 1])
      d[i] = min(min(d[i - 1], d[i]) + 1, prev + cost)
      prev = old
  
  # Return Levenshtein distance
  return d[len(s)]

# Example usage:
# s = "kitten"
# t = "sitting"
# k = 3

# distance = levenshtein_distance(s, t, k)
# print(f"Levenshtein distance: {distance}")

def levenshtein_distance_memopt(s: str, t: str) -> int:
  m, n = len(s), len(t)
  
  # Создаем два рабочих массива целочисленных расстояний
  v0 = list(range(n + 1))
  v1 = [0] * (n + 1)

  for i in range(m):
    # Вычисляем v1 (текущую строку расстояний) из предыдущей строки v0

    # Первый элемент v1 - это A[i + 1][0]
    # Расстояние редактирования - удаление (i + 1) символов из s для соответствия пустому t
    v1[0] = i + 1

    # Используем формулу для заполнения остальной части строки
    for j in range(n):
      # Расчет стоимостей для A[i + 1][j + 1]
      deletion_cost = v0[j + 1] + 1
      insertion_cost = v1[j] + 1
      if s[i] == t[j]:
        substitution_cost = v0[j]
      else:
        substitution_cost = v0[j] + 1

      v1[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)

    # Копируем v1 (текущую строку) в v0 (предыдущую строку) для следующей итерации
    # Поскольку данные в v1 всегда аннулируются, обмен без копирования может быть более эффективным
    v0, v1 = v1, v0

  # После последнего обмена результаты v1 теперь находятся в v0
  return v0[n]

def levenstein_similarity(s: str, t: str) -> float:
  distance = levenshtein_distance_memopt(s, t)
  return 1 - distance / max(len(s), len(t))


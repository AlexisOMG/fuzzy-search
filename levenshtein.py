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
s = "kitten"
t = "sitting"
k = 3

distance = levenshtein_distance(s, t, k)
print(f"Levenshtein distance: {distance}")

def damerau_levenshtein_distance(A, B):
  n = len(A)
  m = len(B)

  F = [[0] * (m + 1) for i in range(n + 1)]

  for i in range(n + 1):
    F[i][0] = i

  for j in range(m + 1):
    F[0][j] = j

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      F[i][j] = min(F[i - 1][j], F[i][j - 1]) + 1
      F[i][j] = min(F[i][j], F[i - 1][j - 1] + int(A[i - 1] != B[j - 1]))
      if i >= 2 and j >= 2 and A[i - 2:i] == B[j - 2:j][::-1]:
        F[i][j] = min(F[i][j], F[i - 2][j - 2] + 1)

  return F[n][m]

print(damerau_levenshtein_distance("XABCDE", "ACBYDF"))       # 4
print(damerau_levenshtein_distance("programma", "pogarmmma")) # 3

def damerau_levenshtein_distance(s, t, delete_cost, insert_cost, replace_cost, transpose_cost):
    m, n = len(s), len(t)
    
    if s == "":
      return n
    elif t == "":
      return m
    
    inf = (m + n) * max(delete_cost, insert_cost, replace_cost, transpose_cost)
    d = [[inf] * (n + 2) for _ in range(m + 2)]
    
    for i in range(m + 1):
      d[i + 1][1] = i * delete_cost
      d[i + 1][0] = inf
        
    for j in range(n + 1):
      d[1][j + 1] = j * insert_cost
      d[0][j + 1] = inf
        
    last_position = {}
    for letter in (s + t):
      last_position[letter] = 0
        
    for i in range(1, m + 1):
      last = 0
      for j in range(1, n + 1):
        i_ = last_position[t[j - 1]]
        j_ = last
        
        if s[i - 1] == t[j - 1]:
          d[i + 1][j + 1] = d[i][j]
          last = j
        else:
          d[i + 1][j + 1] = min(d[i][j] + replace_cost, d[i + 1][j] + insert_cost, d[i][j + 1] + delete_cost)
            
        d[i + 1][j + 1] = min(
          d[i + 1][j + 1], 
          d[i_][j_] + (i - i_ - 1) * delete_cost + transpose_cost + (j - j_ - 1) * insert_cost
        )
          
      last_position[s[i - 1]] = i
        
    return d[m][n]

def levenshtein_distance(s: str, t: str) -> int:
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

